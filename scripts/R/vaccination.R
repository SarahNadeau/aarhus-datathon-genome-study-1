
vacc_load_data <- function () {
  data <- read_csv(
    url("https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/vaccinations.csv"),
    col_types = cols(
      "location" = col_character(),
      "iso_code" = col_character(),
      "date" = col_date(),
      "total_vaccinations" = col_double(),
      "people_vaccinated" = col_double(),
      "people_fully_vaccinated" = col_double(),
      "total_boosters" = col_double(),
      "daily_vaccinations_raw" = col_double(),
      "daily_vaccinations" = col_double(),
      "total_vaccinations_per_hundred" = col_double(),
      "people_vaccinated_per_hundred" = col_double(),
      "people_fully_vaccinated_per_hundred" = col_double(),
      "total_boosters_per_hundred" = col_double(),
      "daily_vaccinations_per_million" = col_double()
    )
  ) %>%
    filter(iso_code %in% c("DNK", "CHE", "ZAF")) %>%
    mutate(
      date = ymd(date)
    ) %>%
    rename(
      country = location
    ) %>%
    drop_na(total_vaccinations) %>%
    replace_na(list(
      people_vaccinated = 0,
      people_fully_vaccinated = 0
    ))

  return(data)
}
