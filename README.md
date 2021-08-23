## Sequencing project 1

This project aims to visualize population-level SARS-CoV-2 diversity in comparison with vaccination rates in Denmark and Switzerland.

### Project structure
Configuration variables are specified in the [configuration file](config.yaml).
A [main bash script](scripts/main.sh) calls [python scripts](scripts/python) to generate the data.
The data is visualized using [R scripts](scripts/R).

### Usage
* Clone this repository
* Create a `data` directory containing:
    * `metadata_snpeff_tidy_<country>.tsv`: GISAID metadata provided by the datathon organizers (requires GISAID account to use)
    * `mutations_snpeff_annotated_tidy_<country>.tsv`: per-sample mutation data provided by the datathon organizers (same GISAID limitation)
    * [owid-covid-data.csv](https://github.com/owid/covid-19-data/blob/master/public/data/owid-covid-data.csv): Full COVID-19 data set from Our World in Data
* Edit the configurations in [config.yaml](config.yaml) as desired
* Change the -m input in [main.sh](scripts/main.sh) to the appropriate country's mutation data file
* Run `bash scripts/main.sh` in your command line
* Run the [visualization R script](scripts/R/report.Rmd) in your IDE of choice to generate an HTML report
