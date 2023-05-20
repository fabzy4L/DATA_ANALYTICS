

# Load R packages
library(shiny)
library(shinythemes)
library(ggplot2)
library(DT)

# Define UI layout
ui <- fluidPage(theme = shinytheme("cosmo"),  
                titlePanel(
                  h1("GENOMICS TOOLS")
                ),
                navbarPage(
                  "Genomic Testing",
                  tabPanel("DATA",
                           sidebarPanel(
                             tags$h3("Submit a Request:"),
                             helpText("Demographic information."),
                             textInput("txt1", "First Name:", ""),
                             textInput("txt2", "Last Name:", ""),
                             selectInput('txt4', label = 'Select Service', 
                                         choices = c("Genomic Testing", "Genomic Analysis")),
                             fileInput("file1", "Choose CSV File",
                                       accept = c("text/csv", 
                                                  "text/comma-separated-values,text/plain", ".csv")),
                             tags$hr(),
                             checkboxInput("header", "Header", TRUE),
                             actionButton("submit", "Submit"),
                             uiOutput("xvar_select"),
                             uiOutput("yvar_select")
                           ), 
                           mainPanel(
                             h1("Review Information:"), 
                             h4("Output:"),
                             helpText("Please make sure the file contains RSIDs"),
                             h1(" "),
                             verbatimTextOutput("txtout"), 
                             verbatimTextOutput("txtout4"), 
                             verbatimTextOutput("txtout3"), 
                             plotOutput("plot1"),
                             DTOutput('dto')
                           )
                  ) 
                ))


# Define server function
server <- function(input, output, session) {
  
  output$txtout <- renderText({
    paste( "Name:", input$txt1, input$txt2, sep=" " )
  })
  
  output$txtout3 <- renderText({
    paste0( "File:", input$file1, sep = " " )
  })
  
  output$txtout4 <- renderText({
    paste0('Service: ', input$txt4)
  })
  
  # Reactive expression with the data
  contents <- reactive({
    inFile <- input$file1
    if (is.null(inFile)) return(NULL)
    read.csv(inFile$datapath, header = input$header)
  })
  
  # Render data table with buttons extension
  output$dto <- renderDT(contents(), 
                         options = list(dom = 'Bfrtip',
                                        buttons = c('copy', 'csv', 'excel', 'pdf', 'print')))
  
  # Update x-axis variable choices based on uploaded CSV file
  output$xvar_select <- renderUI({
    choices <- colnames(contents())
    selectInput("xvar", "X-axis variable", choices = choices)
  })
  
  # Update y-axis variable choices based on uploaded CSV file
  output$yvar_select <- renderUI({
    choices <- colnames(contents())
    selectInput("yvar", "Y-axis variable", choices = choices)
  })
  
  # Render scatterplot based on input variables
  output$plot1 <- renderPlot({
    ggplot(data = contents(), aes_string(x = input$xvar, y = input$yvar)) +
      geom_point() +
      xlab(input$xvar) +
      ylab(input$yvar)
  })
}

# Run the app
shinyApp(ui = ui, server = server)
