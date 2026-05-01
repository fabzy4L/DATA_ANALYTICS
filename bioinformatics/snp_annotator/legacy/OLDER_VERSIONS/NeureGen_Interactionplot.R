# Load R packages
library(shiny)
library(shinythemes)
library(ggplot2)
library(DT)

# Define UI layout
ui <- fluidPage(theme = shinytheme("cosmo"),  
                titlePanel(
                  h1("NeuReGx")
                ),
                navbarPage(
                  "Genomic Testing",
                  tabPanel("Demographics",
                           sidebarPanel(
                             tags$h3("Submit a Request:"),
                             helpText("Demographic information."),
                             fileInput("file1", "Choose CSV File",
                                       accept = c("text/csv", 
                                                  "text/comma-separated-values,text/plain", ".csv")),
                             selectInput("xcol", "X-axis", NULL),
                             selectInput("ycol", "Y-axis", NULL),
                             selectInput("fillcol", "Fill", NULL),
                             tags$hr(),
                             actionButton("submit", "Submit")
                           ), 
                           mainPanel(
                             h1("Review Information:"), 
                             h4("Output:"),
                             helpText("Please make sure the file contains RSIDs"),
                             h1(" "),
                             verbatimTextOutput("txtout3"), 
                             plotOutput("plot2")
                           )
                  ) 
                ))


# Define server function
server <- function(input, output, session) {
  
  output$txtout3 <- renderText({
    paste0( "File:", input$file1, sep = " " )
  })
  
  # Reactive expression with the data
  contents <- reactive({
    inFile <- input$file1
    if (is.null(inFile)) return(NULL)
    data <- read.csv(inFile$datapath, header = TRUE)
    data$ID <- rownames(data) # Add row names as a new column
    data
  })
  
  observe({
    req(contents())
    updateSelectInput(session, "xcol", choices = colnames(contents()))
    updateSelectInput(session, "ycol", choices = colnames(contents()))
    updateSelectInput(session, "fillcol", choices = colnames(contents()))
  })
  
  # Render interaction plot based on uploaded CSV file
  output$plot2 <- renderPlot({
    ggplot(data = contents(), aes_string(x = input$xcol, y = input$ycol, color = input$fillcol, label = "ID")) +
      geom_point() +
      geom_line() +
      xlab(input$xcol) +
      ylab(input$ycol) +
      scale_color_gradient(low = "white", high = "steelblue", name = input$fillcol) +
      geom_text(check_overlap = TRUE)
  })
  
}

# Run the application
shinyApp(ui = ui, server = server)

