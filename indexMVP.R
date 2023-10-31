#!/usr/bin/Rscript

#if (!require("rMVP")) {
#  install.packages("rMVP")
#  library("rMVP")  # Load the package after installation
#}

library('rMVP')


if (length(args) < 2) {
  cat("\nThis script is for perparing the index file for rMVP. \n")
  cat("Usage: Rscript indexMVP.R <vcf:STR> <IndexName:STR>\n")
  q(status = 1) 
}

args <- commandArgs(trailingOnly=TRUE)
setwd(getwd())
MVP.Data(fileVCF=args[1], fileKin=TRUE, filePC=TRUE, out=args[2]) 
