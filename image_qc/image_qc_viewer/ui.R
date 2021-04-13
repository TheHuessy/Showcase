library(shiny)
library(shinyjs)
library(shinythemes)
library(shinydashboard)

# Define UI for application that draws a histogram
#shinyUI(

shinyUI(fluidPage(
                  titlePanel("Image QC"), ## Could add css that would force this to be fixed like the sidebar
                  sidebarLayout(
                                sidebarPanel(style = "position: fixed; width: inherit;",
                                             width = 3,
                                             uiOutput("sidebar")
                                             ),
                                mainPanel(
                                          uiOutput("mainPage")
                                )
                  )
                  ))





#  fluidPage(shinyjs::useShinyjs(),
#            theme = shinytheme(theme = "slate"),
#            sidebarLayout(
#              sidebarPanel(#style = "position:fixed;width:inherit;",
#                           width = 3
#              ),
            ## Have it start with just the image view, and then add the zoom view (split the main
                          ## page in half to add the zoom bit?
                          ## Have it snap back if we hit a button that also gets shown
                          ## Have the zoomed in portion appear BELOW the thumb
#              mainPanel(width = 9,
#                        uiOutput("SlogOutput")
#              )
#            )
#  )

#  dashboardPage(
#                dashboardHeader(title = ),
#                dashboardSidebar(),
#                dashbaordBody()
#                )

#)
