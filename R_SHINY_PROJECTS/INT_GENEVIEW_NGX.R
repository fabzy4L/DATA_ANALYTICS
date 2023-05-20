library(shiny)
library(data.table)
library(RCurl)
library(randomForest)
library(dplyr)
library(tidyverse)
library(biomaRt)

ui <- fluidPage(theme = shinytheme("cosmo"),  
                titlePanel(h1("GENOMICS TOOLS")), 
                navbarPage("Genomic Testing",
                           tabPanel("DATA",
                                    sidebarLayout(
                                      sidebarPanel(
                                        fileInput("file1", "Choose CSV File",
                                                  accept = c("text/csv",
                                                             "text/comma-separated-values,text/plain",
                                                             ".csv")),
                                        br(),
                                        actionButton("processBtn", "Process"),
                                        downloadButton("downloadData", "Download Processed Data")
                                      ),
                                      mainPanel(
                                        h1("Review Information:"), 
                                        h4("Output:"),
                                        helpText("Please make sure the file contains 200 RSIDs at a time"),
                                        h1(" "),
                                        tableOutput("processedDataTable")
                                      )
                                    )
                           )
                ))

server <- function(input, output) {
  
  data <- reactive({
    req(input$file1)
    inFile <- input$file1
    
    if (is.null(inFile))
      return(NULL)
    
    read.csv(inFile$datapath)
  })
  
  processedData <- eventReactive(input$processBtn, {
    dna1 <- data()
    
    ensembl <- useMart("ENSEMBL_MART_SNP", dataset= "hsapiens_snp")
    myfilters <- listFilters(ensembl)
    filter1 <- 'snp_filter'
    attributes1 <- listAttributes(ensembl)
    att1 <- c('refsnp_id','snp','allele','chr_name', 'minor_allele', 'minor_allele_freq','associated_gene','phenotype_description' )
    
    searchResults <- getBM(attributes=att1,
                           filters=filter1,
                           values=dna1, mart=ensembl)
    
    searchResults
  })
  
  output$processedDataTable <- renderTable({
    processedData()
  })
  
  output$downloadData <- downloadHandler(
    filename = function() {
      paste0("processed_data_", Sys.Date(), ".csv")
    },
    content = function(file) {
      write.csv(processedData(), file, row.names = FALSE)
    }
  )
}

shinyApp(ui = ui, server = server)
