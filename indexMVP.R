#!/usr/bin/Rscript

#if (!require("rMVP")) {
#  install.packages("rMVP")
#  library("rMVP")  # Load the package after installation
#}

library('rMVP')

args <- commandArgs(trailingOnly=TRUE)

cat("Arguments received:", args, "\n")

if (length(args) < 2) {
  cat("\nThis script is for preparing the index file for rMVP. \n")
  cat("Usage: Rscript indexMVP.R <vcf:STR> <IndexName:STR>\n")
  quit(status = 1) 
}

MVP.Data(fileVCF=args[1], fileKin=TRUE, filePC=TRUE, out=args[2])
