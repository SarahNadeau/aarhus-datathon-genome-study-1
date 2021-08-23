#' @param filepath Path to diversity_by_time.csv
div_load_data <- function (filepath, dir) {
  data <- read_csv(
    filepath,
    col_types = cols(
      date = col_date(format = "%Y-%m-%d %H:%M:%Z"),
      diversity_measure = col_double()
    )
  ) %>%
    mutate(dir = dir) %>%
    tidyr::separate(col = dir, sep = "_", into = c('iso_code', 'lineage'), remove = F)
  return(data)
}
