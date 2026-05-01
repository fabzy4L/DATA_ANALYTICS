install.packages(c("shiny", "dplyr", "ggplot2", "leaflet"))

library(shiny)
library(dplyr)
library(ggplot2)
library(leaflet)

ui <- fluidPage(
  titlePanel("Disease Outbreak Tracker"),
  sidebarLayout(
    sidebarPanel(
      selectInput("region", "Select Region:",
                  choices = c("All", "Region A", "Region B", "Region C")),
      sliderInput("cases", "Select Minimum Cases:",
                  min = 0, max = 1000, value = 0),
      sliderInput("deaths", "Select Minimum Deaths:",
                  min = 0, max = 100, value = 0),
      sliderInput("recovered", "Select Minimum Recovered:",
                  min = 0, max = 1000, value = 0),
      selectInput("variable", "Select Variable:",
                  choices = c("Cases", "Deaths", "Recovered"))
    ),
    mainPanel(
      tabsetPanel(
        tabPanel("Table", dataTableOutput("table")),
        tabPanel("Map", leafletOutput("map")),
        tabPanel("Graph", plotOutput("graph"))
      )
    )
  )
)

server <- function(input, output) {
  
  # Load data
  outbreak <- read.csv(text = getURL("https://raw.githubusercontent.com/fabzy4L/DATA_ANALYTICS/main/EPIDEMIOLOGY_COV19_SHINY/outbreak.csv"))
  outbreak$Region <- factor(outbreak$Region)
  
  # Filter data based on user input
  filtered <- reactive({
    if (input$region == "All") {
      filtered <- outbreak
    } else {
      filtered <- filter(outbreak, Region == input$region)
    }
    filtered <- filter(filtered, Cases >= input$cases,
                       Deaths >= input$deaths, Recovered >= input$recovered)
    filtered
  })
  
  # Display table
  output$table <- renderDataTable({
    filtered()
  })
  
  # Display map
  output$map <- renderLeaflet({
    leaflet(filtered()) %>%
      addTiles() %>%
      addMarkers(~Longitude, ~Latitude, popup = ~paste("Cases: ", Cases,
                                                       "<br>Deaths: ", Deaths, "<br>Recovered: ", Recovered))
  })
  
  # Display graph
  output$graph <- renderPlot({
    ggplot(filtered(), aes(x = Region, y = .data[[input$variable]], fill = Region)) +
      geom_bar(stat = "identity", position = "dodge") +
      xlab("Region") +
      ylab(input$variable) +
      ggtitle("Disease Outbreak Tracker")
  })
  
  # Display graph
  #  output$graph <- renderPlot({
  #   ggplot(filtered(), aes(x = Region, y = .data[[input$variable]], fill = Region)) +
  #      geom_histogram(position = "dodge", binwidth = 50) +
  #      xlab("Region") +
  #      ylab(input$variable) +
  #      ggtitle("Disease Outbreak Tracker")
  #  })
  
  
}

shinyApp(ui = ui, server = server)

