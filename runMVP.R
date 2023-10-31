#!/usr/bin/Rscript

#if (!require("rMVP")) {
#  install.packages("rMVP")
#  library("rMVP")  # Load the package after installation
#}

library('rMVP')


if (length(args) < 4) {
  cat("\nUsage: Rscript runMVP.R <PhenotypeFile> <IndexName> <Threshold> <ModelName>\n")
  q(status = 1) 
}


args <- commandArgs(trailingOnly=TRUE)
setwd(getwd())
genotype <- attach.big.matrix(paste(args[2], ".geno.desc"))
phenotype  <- read.table(args[1], header = TRUE, sep='\t')
map <- read.table(paste(args[2], ".geno.map" , head = TRUE)
Kinship <- attach.big.matrix(paste(args[2], ".kin.desc")
Covariates <- bigmemory::as.matrix(attach.big.matrix(paste(args[2], ".pc.desc"))

for(i in 2:ncol(phenotype)){
  imMVP <- MVP(
    phe=phenotype[, c(1, i)],
    geno=genotype,
    map=map,
    K=Kinship,
    CV.FarmCPU=Covariates,
    priority="speed",
    ncpus=5,
    vc.method="BRENT",
    maxLoop=10,
    method.bin="static",
    threshold=as.numeric(args[3]),#as.numeric(args[1])
    #method=c("GLM", "MLM", "FarmCPU")
    method=args[4]#"FarmCPU"
  )
  gc()
}


