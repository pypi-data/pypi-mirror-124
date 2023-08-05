from Exceptions import InvalidModeException
from Modes import PDF_Modes
import PyPDF2

class PDFFileHandler:
    def __init__(self,path:str,mode:str=PDF_Modes.READ):
        self.path = path
        self.mode = mode
        self.file = open(self.path,mode)
        self.mode = PDF_Modes.READ
        
    def readPDFPage(self,page_no:int):
        if self.mode == PDF_Modes.READ:
            pdfReader = PyPDF2.PdfFileReader(self.file)
            page = pdfReader.getPage(page_no)
            pdfReader.close()
            return page.extractText()
    
    def readPDFAllPages(self):
        if self.mode == PDF_Modes.READ:
            pdfReader = PyPDF2.PdfFileReader(self.file)
            totalPgs = pdfReader.getNumPages()
            data = []
            for i in range(0,totalPgs):
                page = pdfReader.getPage(i)
                data.append(page.extractText())
            pdfReader.close()
            return data

    def PDFrotate(self, newFilePath:str,rotationAngle:float):
        if self.mode == PDF_Modes.ROTATE:
            pdf = open(self.file, PDF_Modes.ROTATE)
            pdfReader = PyPDF2.PdfFileReader(pdf)
            pdfWriter = PyPDF2.PdfFileWriter()
            
            for page in range(pdfReader.numPages):
                pageObj = pdfReader.getPage(page)
                pageObj.rotateClockwise(rotationAngle)
                pdfWriter.addPage(pageObj)
    
    def mergePDF(self, outputFilePath):
        if self.mode == PDF_Modes.MERGE:
            pdfMerger = PyPDF2.PdfFileMerger()
            pdfMerger.append(self.file)

            with open(outputFilePath, PDF_Modes.MERGE) as f:
                pdfMerger.write(f)

    def splitPDF(self, splits):
        pdfFileObj = open(self.file.name, PDF_Modes.SPLIT)
        pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
        start = 0
        end = splits[0]
        pdfs = []
        for i in range(len(splits)+1):
            pdfWriter = PyPDF2.PdfFileWriter()
            outputpdf = self.file.name.split('.pdf')[0] + str(i) + '.pdf'
            for page in range(start,end):
                pdfWriter.addPage(pdfReader.getPage(page))
            with open(outputpdf, "wb") as f:
                pdfWriter.write(f)
            start = end
            try:
                end = splits[i+1]
            except IndexError:
                end = pdfReader.numPages
            pdfs.append(outputpdf)
        pdfFileObj.close()

        return pdfs
    