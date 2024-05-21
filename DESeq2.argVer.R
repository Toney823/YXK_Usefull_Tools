#!/bin/Rscript
if (!requireNamespace("DESeq2", quietly = TRUE)) {
  if (!requireNamespace("BiocManager", quietly = TRUE))
    install.packages("BiocManager")
  library(BiocManager)
  BiocManager::install("DESeq2")
}
library(DESeq2)
if (!requireNamespace("ggplot2", quietly = TRUE)) {
  BiocManager::install("ggplot2")
}
library(ggplot2)
if (!requireNamespace("ggrepel", quietly = TRUE)) {
  BiocManager::install("ggrepel")
}
library(ggrepel)

args <- commandArgs(trailingOnly = TRUE)

if (length(args) < 3) {
  stop(paste("Usage: \n\t Rscript ","DESeq2.argVer.R", " countMatrix<FilePath:STR> groupMatrix<FilePath:STR> outPath<DirPathSTR>"))
}


countMatrix <- args[1]
groupsMatrix <- args[2]
outPath <- args[3]


mycounts <- read.table(countMatrix, sep = '\t', header = 1, check.names=FALSE)
rownames(mycounts)<-mycounts[,1]
mycounts<-mycounts[,-1]
colData<-read.csv(groupsMatrix, row.names = 1, sep = '\t')

all(rownames(colData) == colnames(mycounts))
condition <- factor(colData$condition)
condition = relevel( condition, "ref")
mycounts[is.na(mycounts)] <- 0
dds <- DESeqDataSetFromMatrix(round(mycounts), colData, design= ~ condition)
dds <- DESeq(dds)
res <- results(dds, contrast = c('condition', 'alt', 'ref'))
res = res[order(res$pvalue),]
write.csv(res,file=paste(outPath,"01_allresults.csv", sep = ''),quote = FALSE)
res[which(res$log2FoldChange >= 1 & res$padj < 0.05),'sig'] <- 'up'
res[which(res$log2FoldChange <= -1 & res$padj < 0.05),'sig'] <- 'down'
res [which(abs(res$log2FoldChange) <= 1 | res$padj >= 0.05),'sig'] <- 'none'
write.csv(res,file=paste(outPath, "02_log2FCandPfilted.csv", sep = ''),quote = FALSE)

res_up <- subset(res, sig == 'up')
res_down <- subset(res, sig == 'down')

write.csv(res_up, file = paste(outPath,'03_gene_up.csv', sep = ''))
write.csv(res_down, file = paste(outPath,'03_gene_down.csv', sep = ''))


dat<-as.data.frame(res)
pdf(paste(outPath, "04_volcano_plot.pdf", sep = ''),height=12,width=11)
ggplot(dat,aes(x=log2FoldChange,y=-log10(padj),color=sig))+
  geom_point()+
  scale_color_manual(values=c("#CC0000","#BBBBBB","#2f5688"))+
  theme_bw()+
  theme(
    legend.title = element_blank()
  )+
  theme(axis.title.x =element_text(size=14,face = "bold"), axis.title.y=element_text(size=14,face = "bold"),axis.text = element_text(size = 14,face = "bold")) +  #调整坐标轴字号
  ylab('-log10 (p-adj)')+
  xlab('log2 (FoldChange)')+
  geom_vline(xintercept=c(-1,1),lty=3,col="black",lwd=0.5) +  #添加垂直阈值|FoldChange|>2
  geom_hline(yintercept = -log10(0.05),lty=3,col="black",lwd=0.5)  #添加水平阈值padj<0.05
dev.off()


