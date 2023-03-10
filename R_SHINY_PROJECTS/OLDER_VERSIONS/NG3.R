library(shiny)
library(readxl)

ui <- fluidPage(
  titlePanel("Neural Progenitor Cell Gene Expression Analysis"),
  sidebarLayout(
    sidebarPanel(
      fileInput("file", "Upload Data",
                accept = c(".csv", ".xlsx")),
      checkboxInput("header", "Header", TRUE),
      radioButtons("sep", "Separator",
                   choices = c(Comma = ",", Semicolon = ";", Tab = "\t"), selected = ","),
      radioButtons("quote", "Quote",
                   choices = c(None = "", "Double Quote" = '"', "Single Quote" = "'"), selected = '"'),
      actionButton("submit", "Submit")
    ),
    mainPanel(
      tableOutput("data")
    )
  )
)

server <- function(input, output) {
  data <- reactive({
    req(input$file)
    infile <- input$file
    if (tolower(substr(infile$name, nchar(infile$name)-3, nchar(infile$name))) == "xlsx") {
      data <- read_excel(infile$datapath)
    } else {
      data <- read.csv(infile$datapath,
                       header = input$header,
                       sep = input$sep,
                       quote = input$quote,
                       stringsAsFactors = FALSE)
    }
    return(data)
  })
  
  output$data <- renderTable({
    data()
  })
}

shinyApp(ui, server)
