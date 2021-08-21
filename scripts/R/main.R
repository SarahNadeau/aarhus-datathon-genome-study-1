library(tidyverse)
library(lubridate)
source("vaccination.R")
source("diversity.R")

# Load data
vacc_data <- vacc_load_data()
div_data <- div_load_data("../../temp/CHE/diversity_by_time.csv")
