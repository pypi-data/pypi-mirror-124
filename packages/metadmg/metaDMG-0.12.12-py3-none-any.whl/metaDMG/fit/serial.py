import pandas as pd
from pathlib import Path
import subprocess
import shlex
import shutil
from logger_tt import logger
from multiprocessing import current_process

# import json
from collections import Counter
from metaDMG.loggers.loggers import setup_logger
from metaDMG.errors import metadamageError
from metaDMG.fit import mismatches, fits, results

#%%


def do_run(targets, forced=False):

    if forced:
        logger.info("Using forced load, beware.")

    if forced:
        return True

    if not isinstance(targets, list):
        targets = [targets]

    if all(Path(target).exists() for target in targets):
        return False
    else:
        return True


def do_load(targets, forced=False):
    return not do_run(targets, forced=forced)


def data_dir(config, name, suffix="parquet"):
    target = Path(config["dir"]) / name / f"{config['sample']}.{name}.{suffix}"
    return str(target)


#%%


def get_LCA_command(config):
    sample = config["sample"]
    bam = config["samples"][sample]
    lca_rank = f"-lca_rank {config['lca_rank']}" if config["lca_rank"] != "" else ""

    command = (
        f"{config['metaDMG-lca']} lca "
        f"-bam {bam} "
        f"-outnames {sample} "
        f"-names {config['names']} "
        f"-nodes {config['nodes']} "
        f"-acc2tax {config['acc2tax']} "
        f"-simscorelow {config['simscorelow']} "
        f"-simscorehigh {config['simscorehigh']} "
        f"-editdistmin {config['editdistmin']} "
        f"-editdistmax {config['editdistmax']} "
        f"{lca_rank} "
        f"-minmapq {config['minmapq']} "
        f"-howmany {config['max_position']} "
        f"-weighttype {config['weighttype']} "
        f"-fix_ncbi {config['fix_ncbi']} "
    )
    return command[:-1]


def get_LCA_mismatches_command(config):
    sample = config["sample"]
    bdamage = f"{sample}.bdamage.gz"
    lca_stat = f"{sample}.lca.stat"

    command = (
        f"{config['metaDMG-lca']} print_ugly "
        f"{bdamage} "
        f"-names {config['names']} "
        f"-nodes {config['nodes']} "
        f"-lcastat {lca_stat} "
    )
    return command[:-1]


#%%


def move_files(config):
    sample = config["sample"]

    d_move_source_target = {
        f"{sample}.bdamage.gz.uglyprint.mismatch.txt": config["path_mismatches_txt"],
        f"{sample}.bdamage.gz.uglyprint.stat.txt": config["path_mismatches_stat"],
        f"{sample}.lca": config["path_lca"],
    }
    for source_path, target_path in d_move_source_target.items():
        logger.debug(f"Moving {source_path} to {target_path}.")
        if not Path(source_path).exists():
            raise metadamageError(f"{source_path} does not exist.")
        Path(target_path).parent.mkdir(parents=True, exist_ok=True)
        shutil.move(source_path, target_path)


def delete_files(config):
    sample = config["sample"]

    bam = Path(config["samples"][sample]).stem  # .name

    paths_to_remove = [
        f"{sample}.lca.stat",
        f"{sample}.bdamage.gz",
        f"{sample}.log",
        *list(Path(".").glob(f"*{bam}*.bin")),
    ]
    for path in paths_to_remove:
        logger.debug(f"Removing {path}.")
        if not Path(path).exists():
            raise metadamageError(f"{path} does not exist.")
        Path(path).unlink()


#%%


def run_command(command):

    p = subprocess.Popen(
        shlex.split(command),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    for line in iter(p.stdout.readline, b""):
        if line:
            line = line.decode("utf-8")
            if line.endswith("\n"):
                line = line[:-1]
            yield line

    # waits for the process to finish and returns the returncode
    yield p.wait()


def run_command_helper(config, command):

    # add a counter to avoid too many similar lines
    counter = Counter()
    for line in run_command(command):

        # if finished, check returncode
        if isinstance(line, int):
            returncode = line
            if returncode != 0:
                s = config["metaDMG-lca"] + "did not terminate properly."
                raise metadamageError(s)

        # continue running and logging
        if counter[line] < 3:
            logger.debug(line)

        # do not print the same line more than 3 times
        elif counter[line] == 3:
            logger.debug("...")
            logger.debug("...")
            logger.debug("...")

        counter[line] += 1


#%%


def run_LCA(config, forced=False):

    logger.info(f"Getting LCA.")

    targets = [
        config["path_mismatches_txt"],
        config["path_mismatches_stat"],
        config["path_lca"],
    ]

    if do_run(targets, forced=forced):
        logger.info(f"LCA has to be computed. This can take a while, please wait.")

        command_LCA = get_LCA_command(config)
        command_LCA_mismatches = get_LCA_mismatches_command(config)

        logger.debug(command_LCA)
        run_command_helper(config, command_LCA)

        logger.debug(command_LCA_mismatches)
        run_command_helper(config, command_LCA_mismatches)

        move_files(config)
        delete_files(config)

    else:
        logger.info(f"LCA already been run before.")


#%%


def get_df_mismatches(config, forced=False):

    logger.info(f"Getting df_mismatches")

    target = data_dir(config, name="mismatches")

    if do_run(target, forced=forced):
        logger.info(f"Computing df_mismatches.")
        df_mismatches = mismatches.compute(config)
        Path(target).parent.mkdir(parents=True, exist_ok=True)
        df_mismatches.to_parquet(target)

    else:
        logger.info(f"Loading df_mismatches.")
        df_mismatches = pd.read_parquet(target)

    return df_mismatches


#%%


def dataframe_columns_contains(df, s):
    return any(s in column for column in df.columns)


def get_df_fit_results(config, df_mismatches, forced=False):

    logger.info(f"Getting df_fit_results.")

    target = data_dir(config, name="fit_results")
    if do_load(target, forced=forced):
        logger.info(f"Try to load df_fit_results.")
        df_fit_results = pd.read_parquet(target)

        # if frequentist fits only, return immediately
        if not config["bayesian"]:
            logger.info(f"Loading df_fit_results (frequentist).")
            return df_fit_results

        # if df_fit_results has already been run with Bayesian, return this
        if dataframe_columns_contains(df_fit_results, "Bayesian"):
            logger.info(f"Loading df_fit_results (Bayesian).")
            return df_fit_results

    # Compute the fits
    info = "Fitting the data"
    if config["bayesian"]:
        info += " with a Bayesian model, please wait."
    else:
        info += " with a frequentist (MAP) model."

    logger.info(info)
    df_fit_results = fits.compute(config, df_mismatches)
    Path(target).parent.mkdir(parents=True, exist_ok=True)
    df_fit_results.to_parquet(target)

    return df_fit_results


#%%


def get_df_results(config, df_mismatches, df_fit_results, forced=False):

    logger.info(f"Getting df_results.")

    target = data_dir(config, name="results")

    if do_load(target, forced=forced):
        logger.info(f"Loading df_results.")
        df_results = pd.read_parquet(target)

        # if frequentist fits only, return immediately
        if not config["bayesian"]:
            return df_results

        # if df_results has already been run with Bayesian, return this
        if dataframe_columns_contains(df_results, "Bayesian"):
            return df_results

    # Compute the results:
    logger.info(f"Computing df_results.")
    df_results = results.merge(df_mismatches, df_fit_results)
    Path(target).parent.mkdir(parents=True, exist_ok=True)
    df_results.to_parquet(target)

    return df_results


#%%


def run_single_config(config):

    # if not main process (and haven't been initialized before)
    name = current_process().name
    if "SpawnPoolWorker" in name or "SpawnProcess" in name:
        setup_logger(
            log_port=config["log_port"],
            log_path=config["log_path"],
        )

    current_process().name = config["sample"]

    try:
        run_LCA(config)
    except metadamageError as error:
        logger.exception(f"{config['sample']} | metadamageError with run_LCA.")
        return None

    df_mismatches = get_df_mismatches(config)
    df_fit_results = get_df_fit_results(config, df_mismatches)
    df_results = get_df_results(config, df_mismatches, df_fit_results)
    # read_ids_mapping = get_database_read_ids(config)

    logger.info("Finished.")
    return df_mismatches, df_fit_results, df_results
