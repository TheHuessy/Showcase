library(shiny)
library(shinyjs)
library(shinythemes)
library(shinydashboard)

shinyUI(
        dashboardPage(skin = "purple",
                      dashboardHeader(title = "Image QC Tool"),
                      dashboardSidebar(
                                             uiOutput("sidebar"),
                                             uiOutput("image_info")
                                             ),
                      dashboardBody(tags$head(
                                              tags$link(rel = "stylesheet",
                                                        type = "text/css",
                                                        href = "custom.css"
                                              )
                                              ),
                                          uiOutput("mainPage"),
                                          tags$br()
                                )
                  )
)

