ckan.module('ckan-content-ckeditor', function ($) {
  return {
    options: {
        site_url: ""
      },

    initialize: function () {
      jQuery.proxyAll(this, /_on/);
      this.el.ready(this._onReady);
    },

    _onReady: function(){
        // console.log(CKEditor);
        // CKANCKEditor5
        CKANCKEditor5.initEditor(this.el[0]);
    //     const editorConfig = {
    //         toolbar: {
    //             items: [
    //                 'undo',
    //                 'redo',
    //                 '|',
    //                 'sourceEditing',
    //                 'showBlocks',
    //                 'findAndReplace',
    //                 'fullscreen',
    //                 '|',
    //                 'heading',
    //                 '|',
    //                 'fontSize',
    //                 'fontFamily',
    //                 'fontColor',
    //                 'fontBackgroundColor',
    //                 '|',
    //                 'bold',
    //                 'italic',
    //                 'underline',
    //                 'strikethrough',
    //                 'superscript',
    //                 'code',
    //                 '|',
    //                 'horizontalLine',
    //                 'link',
    //                 'insertImageViaUrl',
    //                 'mediaEmbed',
    //                 'insertTable',
    //                 'highlight',
    //                 'blockQuote',
    //                 'codeBlock',
    //                 'htmlEmbed',
    //                 '|',
    //                 'alignment',
    //                 '|',
    //                 'bulletedList',
    //                 'numberedList'
    //             ],
    //             shouldNotGroupWhenFull: true
    //         },
    //         plugins: [
    //             CKEDITOR.Alignment,
    //             CKEDITOR.AutoImage,
    //             CKEDITOR.AutoLink,
    //             CKEDITOR.Autosave,
    //             CKEDITOR.BalloonToolbar,
    //             CKEDITOR.BlockQuote,
    //             CKEDITOR.Bold,
    //             CKEDITOR.CloudServices,
    //             CKEDITOR.Code,
    //             CKEDITOR.CodeBlock,
    //             CKEDITOR.Essentials,
    //             CKEDITOR.FindAndReplace,
    //             CKEDITOR.FontBackgroundColor,
    //             CKEDITOR.FontColor,
    //             // CKEDITOR.FontFamily,
    //             CKEDITOR.FontSize,
    //             CKEDITOR.Fullscreen,
    //             CKEDITOR.GeneralHtmlSupport,
    //             CKEDITOR.Heading,
    //             CKEDITOR.Highlight,
    //             CKEDITOR.HorizontalLine,
    //             CKEDITOR.HtmlComment,
    //             CKEDITOR.HtmlEmbed,
    //             CKEDITOR.ImageBlock,
    //             CKEDITOR.ImageCaption,
    //             CKEDITOR.ImageInline,
    //             CKEDITOR.ImageInsertViaUrl,
    //             CKEDITOR.ImageResize,
    //             CKEDITOR.ImageStyle,
    //             CKEDITOR.ImageTextAlternative,
    //             CKEDITOR.ImageToolbar,
    //             CKEDITOR.ImageUpload,
    //             CKEDITOR.Italic,
    //             CKEDITOR.Link,
    //             CKEDITOR.LinkImage,
    //             CKEDITOR.List,
    //             CKEDITOR.ListProperties,
    //             CKEDITOR.MediaEmbed,
    //             CKEDITOR.Paragraph,
    //             CKEDITOR.ShowBlocks,
    //             CKEDITOR.SourceEditing,
    //             CKEDITOR.Strikethrough,
    //             CKEDITOR.Superscript,
    //             CKEDITOR.Table,
    //             CKEDITOR.TableCaption,
    //             CKEDITOR.TableCellProperties,
    //             CKEDITOR.TableColumnResize,
    //             CKEDITOR.TableProperties,
    //             CKEDITOR.TableToolbar,
    //             CKEDITOR.Underline
    //         ],
    //         balloonToolbar: ['bold', 'italic', '|', 'link', '|', 'bulletedList', 'numberedList'],
    //         fontFamily: {
    //             supportAllValues: true
    //         },
    //         fontSize: {
    //             options: [10, 12, 14, 'default', 18, 20, 22],
    //             supportAllValues: true
    //         },
    //         fullscreen: {
    //             onEnterCallback: container =>
    //                 container.classList.add(
    //                     'editor-container',
    //                     'editor-container_classic-editor',
    //                     'editor-container_include-fullscreen',
    //                     'main-container'
    //                 )
    //         },
    //         heading: {
    //             options: [
    //                 {
    //                     model: 'paragraph',
    //                     title: 'Paragraph',
    //                     class: 'ck-heading_paragraph'
    //                 },
    //                 {
    //                     model: 'heading1',
    //                     view: 'h1',
    //                     title: 'Heading 1',
    //                     class: 'ck-heading_heading1'
    //                 },
    //                 {
    //                     model: 'heading2',
    //                     view: 'h2',
    //                     title: 'Heading 2',
    //                     class: 'ck-heading_heading2'
    //                 },
    //                 {
    //                     model: 'heading3',
    //                     view: 'h3',
    //                     title: 'Heading 3',
    //                     class: 'ck-heading_heading3'
    //                 },
    //                 {
    //                     model: 'heading4',
    //                     view: 'h4',
    //                     title: 'Heading 4',
    //                     class: 'ck-heading_heading4'
    //                 },
    //                 {
    //                     model: 'heading5',
    //                     view: 'h5',
    //                     title: 'Heading 5',
    //                     class: 'ck-heading_heading5'
    //                 },
    //                 {
    //                     model: 'heading6',
    //                     view: 'h6',
    //                     title: 'Heading 6',
    //                     class: 'ck-heading_heading6'
    //                 }
    //             ]
    //         },
    //         htmlSupport: {
    //             allow: [
    //                 {
    //                     name: /^.*$/,
    //                     styles: true,
    //                     attributes: true,
    //                     classes: true
    //                 }
    //             ]
    //         },
    //         image: {
    //             toolbar: [
    //                 'toggleImageCaption',
    //                 'imageTextAlternative',
    //                 '|',
    //                 'imageStyle:inline',
    //                 'imageStyle:wrapText',
    //                 'imageStyle:breakText',
    //                 '|',
    //                 'resizeImage'
    //             ]
    //         },
    //         licenseKey: 'GPL',
    //         link: {
    //             addTargetToExternalLinks: true,
    //             defaultProtocol: 'https://',
    //             decorators: {
    //                 toggleDownloadable: {
    //                     mode: 'manual',
    //                     label: 'Downloadable',
    //                     attributes: {
    //                         download: 'file'
    //                     }
    //                 }
    //             }
    //         },
    //         list: {
    //             properties: {
    //                 styles: true,
    //                 startIndex: true,
    //                 reversed: true
    //             }
    //         },
    //         menuBar: {
    //             isVisible: true
    //         },
    //         placeholder: 'Type or paste your content here!',
    //         table: {
    //             contentToolbar: ['tableColumn', 'tableRow', 'mergeTableCells', 'tableProperties', 'tableCellProperties']
    //         }
    //     };

    //     CKEDITOR.ClassicEditor
    //         .create(this.el[0], editorConfig);
    }


  };
});