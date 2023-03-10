library(shiny)
library(epitools)

# Define UI for app
ui <- fluidPage(
  titlePanel("Epidemiology Calculator"),
  sidebarLayout(
    sidebarPanel(
      numericInput("total_population", "Enter total population size:", value = 1000, min = 1),
      numericInput("disease_prevalence", "Enter disease prevalence (%):", value = 5, min = 0, max = 100),
      numericInput("new_cases", "Enter number of new cases:", value = 50, min = 0),
      numericInput("exposed_cases", "Enter number of exposed cases:", value = 150, min = 0),
      actionButton("calculate_button", "Calculate"),
      downloadButton("download_button", "Download results")
    ),
    mainPanel(
      tableOutput("results_table")
    )
  )
)

# Define server logic
server <- function(input, output) {
  
  # Create reactive function for calculating results
  results_data <- reactive({
    prevalence <- input$disease_prevalence / 100
    population_size <- input$total_population
    new_cases <- input$new_cases
    exposed_cases <- input$exposed_cases
    incidence <- new_cases / population_size
    odds_ratio <- oddsratio(matrix(c(new_cases, exposed_cases - new_cases, population_size - exposed_cases - new_cases, exposed_cases), ncol=2))
    
    data.frame(
      "Prevalence" = format(prevalence, digits = 4),
      "Incidence" = format(incidence, digits = 4),
      "Odds Ratio" = format(odds_ratio$measure, digits = 4),
      "95% CI (lower)" = format(odds_ratio$ci[1], digits = 4),
      "95% CI (upper)" = format(odds_ratio$ci[2], digits = 4)
    )
  })
  
  # Render table output
  output$results_table <- renderTable({
    if (input$calculate_button > 0) {
      results_data()
    }
  })
  
  # Download results as CSV file
  output$download_button <- downloadHandler(
    filename = "epidemiology_results.csv",
    content = function(file) {
      write.csv(results_data(), file, row.names = FALSE)
    }
  )
}

# Run the app
shinyApp(ui, server)
