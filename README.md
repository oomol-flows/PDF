# PDF Processing Toolkit

A comprehensive collection of PDF processing blocks for the OOMOL platform, providing powerful tools for document manipulation, conversion, and enhancement.

## 🚀 Overview

This toolkit transforms your OOMOL workspace into a complete PDF processing powerhouse. With 15+ specialized blocks, you can handle everything from basic operations like merging and splitting to advanced features like OCR, form filling, and security management.

## 📦 Available Blocks

### 🔧 **Core PDF Operations**

#### **PDF Watermark** (`pdf_watermark`)
Add professional watermarks to your PDFs with full customization options.
- **Text/Image Watermarks**: Support both text and image overlays
- **Position Control**: Precise placement with X/Y coordinates  
- **Styling Options**: Opacity, rotation, size, color, and font customization
- **Batch Processing**: Apply consistent watermarks across multiple documents

#### **PDF Compression** (`pdf_compress`)
Reduce PDF file sizes while maintaining quality for efficient storage and sharing.
- **Multiple Levels**: Low, medium, high, and maximum compression
- **Smart Optimization**: Image quality adjustment and duplicate removal
- **Size Analytics**: Before/after file size comparison with compression ratios
- **Quality Control**: Maintain document readability while reducing file size

#### **PDF Merge** (`pdf_merge`)  
Combine multiple PDF documents into a single professional document.
- **Batch Merging**: Handle multiple input files simultaneously
- **Bookmark Preservation**: Maintain navigation structure from source documents
- **Page Numbering**: Optionally add sequential page numbers to merged content
- **Metadata Handling**: Preserve document properties and structure

#### **PDF Split** (`pdf_split`)
Divide large PDFs into smaller, manageable files with flexible splitting options.
- **Multiple Split Modes**: Single pages, page ranges, bookmarks, or equal parts
- **Custom Ranges**: Specify exact pages like "1-3,5-7,10"
- **Bookmark-Based**: Automatically split at bookmark boundaries
- **Batch Output**: Generate multiple files with organized naming conventions

### 🔒 **Security & Access Control**

#### **PDF Encryption** (`pdf_encrypt`)
Protect sensitive documents with advanced password and permission controls.
- **Dual Password System**: Separate user and owner passwords
- **Permission Management**: Control printing, copying, and modification rights
- **128-bit Encryption**: Industry-standard security for document protection
- **Batch Security**: Apply consistent security policies across multiple files

#### **PDF Decryption** (`pdf_decrypt`)
Remove password protection from authorized documents.
- **Password Recovery**: Unlock documents with valid credentials
- **Batch Processing**: Decrypt multiple protected files simultaneously
- **Status Reporting**: Verify encryption status and successful decryption
- **Secure Handling**: Safe processing of sensitive document credentials

### 🎨 **Content Manipulation**

#### **PDF Rotation** (`pdf_rotate`)
Correct document orientation with precise page rotation controls.
- **Standard Angles**: 90°, 180°, and 270° rotation options
- **Selective Pages**: Rotate specific pages or page ranges
- **Batch Rotation**: Apply consistent rotation to multiple documents
- **Preview Support**: Visual confirmation before processing

#### **PDF Text Extraction** (`pdf_extract_text`)
Extract and export text content in multiple formats for further processing.
- **Multiple Formats**: Plain text, JSON, or CSV output options
- **Layout Preservation**: Maintain original document formatting
- **Selective Extraction**: Process specific pages or page ranges
- **Batch Export**: Extract text from multiple documents simultaneously

#### **PDF Page Management** (`pdf_delete_pages`, `pdf_insert_pages`)
Fine-tune document structure with advanced page manipulation tools.
- **Page Deletion**: Remove unwanted pages with range specification
- **Page Insertion**: Add content from other PDFs at specific positions  
- **Batch Operations**: Process multiple documents with consistent rules
- **Structure Preservation**: Maintain document integrity during modifications

### 📝 **Interactive Documents**

#### **PDF Form Filling** (`pdf_fill_forms`)
Automate form completion with programmatic field population.
- **Field Detection**: Automatic identification of fillable form fields
- **Data Mapping**: Structured input for consistent form completion
- **Batch Processing**: Fill multiple forms with template data
- **Validation**: Ensure field compatibility and data integrity

#### **PDF Annotation** (`pdf_annotate`)
Enhance documents with professional annotations and markup tools.
- **Multiple Types**: Text, highlights, notes, and custom stamps
- **Precise Positioning**: Coordinate-based placement system
- **Color Customization**: Full color palette for visual organization
- **Collaborative Features**: Professional markup for document review

### 🌐 **Format Conversion**

#### **HTML to PDF** (`html_to_pdf`)
Convert web content and HTML documents to professional PDF format.
- **Multiple Sources**: HTML files, raw strings, or live web URLs
- **Layout Control**: Custom page sizes, orientation, and margins
- **CSS Support**: Full styling preservation during conversion
- **Print Optimization**: Professional output suitable for printing and archiving

### 🔖 **Document Organization**

#### **PDF Bookmark Management** (`pdf_bookmarks`)
Create and manage document navigation with professional bookmark systems.
- **Hierarchical Structure**: Support for nested bookmark organization  
- **Batch Import/Export**: Manage bookmarks across multiple documents
- **Custom Naming**: Flexible bookmark titles and organization
- **Navigation Enhancement**: Improve document usability and accessibility

## 🛠️ Technical Specifications

### **Dependencies**
- **PyPDF/PyPDF2**: Core PDF manipulation engine
- **Reportlab**: Advanced PDF generation and overlay capabilities
- **PDFplumber**: Enhanced text extraction with layout preservation
- **Pytesseract**: Industrial-grade OCR processing
- **WeasyPrint**: Professional HTML to PDF conversion
- **Wand/ImageMagick**: Advanced image processing capabilities

### **Performance Features**
- **Memory Efficient**: Optimized for large file processing
- **Batch Operations**: Handle multiple documents simultaneously
- **Error Handling**: Comprehensive error reporting and recovery
- **Progress Tracking**: Real-time processing status and completion metrics

### **Integration Benefits**
- **OOMOL Native**: Seamless integration with OOMOL workflow system
- **Modular Design**: Mix and match blocks for custom processing pipelines
- **Standard Interfaces**: Consistent input/output formats across all blocks
- **Visual UI**: Intuitive configuration with visual file selectors and controls

## 🎯 Use Cases

### **Business Document Management**
- **Invoice Processing**: Extract text, add watermarks, and secure sensitive financial documents
- **Report Generation**: Merge departmental reports, add page numbers, and apply corporate branding
- **Contract Management**: Fill forms, add annotations, and implement security controls

### **Educational Content**
- **Lecture Materials**: Convert presentation slides, extract reading materials, and organize content
- **Research Papers**: Merge citations, extract references, and apply academic formatting
- **Student Submissions**: Process assignments, add feedback annotations, and manage document collections

### **Digital Publishing**
- **Content Creation**: Convert web articles, add professional layouts, and optimize for distribution
- **Archive Management**: Digitize paper documents with OCR, organize with bookmarks, and secure sensitive materials
- **Portfolio Development**: Merge creative works, add watermarks, and prepare professional presentations

### **Legal and Compliance**
- **Document Redaction**: Remove sensitive information while maintaining document integrity
- **Evidence Management**: Secure documents with encryption, add annotations for case notes
- **Regulatory Submission**: Merge compliance documents, add required metadata, and ensure proper formatting

## 🚦 Getting Started

1. **Install Dependencies**: Ensure all required Python packages are installed via `pip install` or `poetry install`
2. **Import Blocks**: Add desired PDF processing blocks to your OOMOL workflow
3. **Configure Settings**: Customize block parameters for your specific use case
4. **Process Documents**: Execute workflows and monitor processing results
5. **Export Results**: Download processed documents or continue with additional processing steps

## 📈 Advanced Workflows

Combine multiple blocks to create powerful document processing pipelines:

- **Document Digitization**: OCR → Text Extraction → Bookmark Creation
- **Security Pipeline**: Encryption → Watermarking → Compression  
- **Publishing Workflow**: HTML Conversion → Merging → Page Numbering → Final Compression
- **Archive Processing**: Splitting → Individual OCR → Metadata Extraction → Secure Storage

Transform your document processing capabilities with this comprehensive PDF toolkit designed for professional workflows and seamless OOMOL platform integration.