
#install.packages(c("shiny", "data.table", "RCurl", "randomForest", "dplyr", "tidyverse", "biomaRt"))
#allif (!require("BiocManager", quietly = TRUE))
#    install.packages("BiocManager")
#BiocManager::install("biomaRt")
#install.packages("shinythemes")

library(shinythemes)
library(shiny)
library(data.table)
library(RCurl)
library(randomForest)
library(dplyr)
library(tidyverse)
library(biomaRt)
library(DT)

ui <- navbarPage(
  title = "Genomics Tools",
  theme = shinytheme("cosmo"),
  tabPanel(
    "SNP Annotation",
    sidebarLayout(
      sidebarPanel(
        width = 3,
        h4("Upload RSID Data"),
        tags$p(tags$small(
          "Upload a CSV file containing RSIDs (up to 200 at a time). ",
          "The app queries Ensembl BioMart in real time to retrieve allele ",
          "frequencies, chromosome locations, associated genes, and phenotype descriptions."
        )),
        tags$hr(),
        fileInput(
          "file1",
          label    = NULL,
          buttonLabel = "Browse...",
          placeholder = "No file selected",
          accept   = c("text/csv", "text/comma-separated-values,text/plain", ".csv")
        ),
        div(
          style = "display:flex; gap:8px;",
          actionButton("processBtn", "Annotate RSIDs", icon = icon("dna"), class = "btn-primary btn-sm"),
          downloadButton("downloadData", "Export CSV", class = "btn-sm")
        ),
        tags$hr(),
        tags$small(
          tags$b("Minor Allele Frequency key:"), tags$br(), tags$br(),
          tags$span(style = "background:#f28b82; padding:2px 10px; border-radius:3px;", "< 0.05  Rare"), tags$br(), tags$br(),
          tags$span(style = "background:#ffd966; padding:2px 10px; border-radius:3px;", "0.05 – 0.20"), tags$br(), tags$br(),
          tags$span(style = "background:#81c995; padding:2px 10px; border-radius:3px;", "> 0.20  Common")
        )
      ),
      mainPanel(
        width = 9,
        DT::dataTableOutput("processedDataTable")
      )
    )
  )
)

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

    searchResults$snp <- gsub("%", "", searchResults$snp)

    searchResults
  })
  
  output$processedDataTable <- DT::renderDataTable({
    DT::datatable(
      processedData(),
      filter = "top",
      options = list(pageLength = 25, scrollX = TRUE)
    ) %>%
      DT::formatStyle(
        "minor_allele_freq",
        backgroundColor = DT::styleInterval(
          c(0.05, 0.2),
          c("#f28b82", "#ffd966", "#81c995")
        )
      )
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
