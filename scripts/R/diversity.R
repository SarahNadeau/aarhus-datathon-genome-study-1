#' @param filepath Path to diversity_by_time.csv
div_load_data <- function (filepath) {
  data <- read_csv(
    filepath,
    col_types = cols(
      date = col_date(),
      diversity_measure = col_double()
    )
  )
  return(data)
}
