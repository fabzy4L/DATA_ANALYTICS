#LOAD LIBRARY AND INSTALL PACKAGES
library(reticulate)
py_install("pandas")
py_install("numpy")
py_install("scipy")
py_install("matplotlib") #.pylab as plt
pd <- import("pandas")
np <- import("numpy")
sp <- import("scipy")
plt <- import("matplotlib")
library(reticulate)
version <- "3.11"
virtualenv_create("Python", python_version = version)
qpcr = pd$read_csv('/Users/f4L/Library/Containers/com.microsoft.Excel/Data/Desktop/RStudioDataAnalysis/GENE EXPRESSION NICOTINE DATA ANALYSIS/qPCR all values - qPCR.csv')
qpcr
