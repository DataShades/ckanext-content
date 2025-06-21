import ClassicEditor from '@ckeditor/ckeditor5-editor-classic/src/classiceditor.js';

import Essentials from '@ckeditor/ckeditor5-essentials/src/essentials.js';
import Bold from '@ckeditor/ckeditor5-basic-styles/src/bold.js';
import Italic from '@ckeditor/ckeditor5-basic-styles/src/italic.js';
import Underline from '@ckeditor/ckeditor5-basic-styles/src/underline.js';
import Strikethrough from '@ckeditor/ckeditor5-basic-styles/src/strikethrough.js';
import Superscript from '@ckeditor/ckeditor5-basic-styles/src/superscript.js';
import Code from '@ckeditor/ckeditor5-basic-styles/src/code.js';

import Paragraph from '@ckeditor/ckeditor5-paragraph/src/paragraph.js';
import Heading from '@ckeditor/ckeditor5-heading/src/heading.js';

import FontSize from '@ckeditor/ckeditor5-font/src/fontsize.js';
import FontFamily from '@ckeditor/ckeditor5-font/src/fontfamily.js';
import FontColor from '@ckeditor/ckeditor5-font/src/fontcolor.js';
import FontBackgroundColor from '@ckeditor/ckeditor5-font/src/fontbackgroundcolor.js';

import Link from '@ckeditor/ckeditor5-link/src/link.js';
import ImageBlock from '@ckeditor/ckeditor5-image/src/imageblock.js';
import ImageCaption from '@ckeditor/ckeditor5-image/src/imagecaption.js';
import ImageInline from '@ckeditor/ckeditor5-image/src/imageinline.js';
import ImageInsertViaUrl from '@ckeditor/ckeditor5-image/src/imageinsertviaurl.js';
import ImageResize from '@ckeditor/ckeditor5-image/src/imageresize.js';
import ImageStyle from '@ckeditor/ckeditor5-image/src/imagestyle.js';
import ImageTextAlternative from '@ckeditor/ckeditor5-image/src/imagetextalternative.js';
import ImageToolbar from '@ckeditor/ckeditor5-image/src/imagetoolbar.js';
import ImageUpload from '@ckeditor/ckeditor5-image/src/imageupload.js';

import List from '@ckeditor/ckeditor5-list/src/list.js';
import ListProperties from '@ckeditor/ckeditor5-list/src/listproperties.js';

import BlockQuote from '@ckeditor/ckeditor5-block-quote/src/blockquote.js';
import HorizontalLine from '@ckeditor/ckeditor5-horizontal-line/src/horizontalline.js';
import CodeBlock from '@ckeditor/ckeditor5-code-block/src/codeblock.js';
import Table from '@ckeditor/ckeditor5-table/src/table.js';
import TableToolbar from '@ckeditor/ckeditor5-table/src/tabletoolbar.js';
import TableProperties from '@ckeditor/ckeditor5-table/src/tableproperties.js';
import TableCaption from '@ckeditor/ckeditor5-table/src/tablecaption.js';
import TableCellProperties from '@ckeditor/ckeditor5-table/src/tablecellproperties.js';
import TableColumnResize from '@ckeditor/ckeditor5-table/src/tablecolumnresize.js';

import MediaEmbed from '@ckeditor/ckeditor5-media-embed/src/mediaembed.js';
import HtmlEmbed from '@ckeditor/ckeditor5-html-embed/src/htmlembed.js';
import GeneralHtmlSupport from '@ckeditor/ckeditor5-html-support/src/generalhtmlsupport.js';

import SourceEditing from '@ckeditor/ckeditor5-source-editing/src/sourceediting.js';
import ShowBlocks from '@ckeditor/ckeditor5-show-blocks/src/showblocks.js';
import Highlight from '@ckeditor/ckeditor5-highlight/src/highlight.js';
import Autosave from '@ckeditor/ckeditor5-autosave/src/autosave.js';
import Fullscreen from '@ckeditor/ckeditor5-fullscreen/src/fullscreen.js';
import AutoLink from '@ckeditor/ckeditor5-link/src/autolink.js';
import AutoImage from '@ckeditor/ckeditor5-image/src/autoimage.js';
import BalloonToolbar from '@ckeditor/ckeditor5-ui/src/toolbar/balloon/balloontoolbar.js';
import Alignment from '@ckeditor/ckeditor5-alignment/src/alignment.js';


export function initEditor(domElement) {
  ClassicEditor.create(domElement, {
    plugins: [
      Essentials, Bold, Italic, Underline, Strikethrough,
      Superscript, Code, Paragraph, Heading,
      FontSize, FontFamily, FontColor, FontBackgroundColor,
      Link, ImageBlock, ImageCaption, ImageInline,
      ImageInsertViaUrl, ImageResize, ImageStyle,
      ImageTextAlternative, ImageToolbar, ImageUpload,
      List, ListProperties, BlockQuote, HorizontalLine,
      CodeBlock, Table, TableToolbar, TableProperties,
      TableCaption, TableCellProperties, TableColumnResize,
      MediaEmbed, HtmlEmbed, GeneralHtmlSupport,
      SourceEditing, ShowBlocks, Highlight,
      Autosave, Fullscreen, AutoLink, AutoImage,
      BalloonToolbar, Alignment
    ],
    toolbar: {
      items: [
        'undo', 'redo', '|',
        'sourceEditing', 'showBlocks', 'findAndReplace', 'fullscreen', '|',
        'heading', '|',
        'fontSize', 'fontFamily',
        'fontColor', 'fontBackgroundColor', '|',
        'bold', 'italic', 'underline', 'strikethrough',
        'superscript', 'code', '|',
        'horizontalLine', 'link', 'insertImageViaUrl',
        'mediaEmbed', 'insertTable', 'highlight',
        'blockQuote', 'codeBlock', 'htmlEmbed', '|',
        'alignment', '|',
        'bulletedList', 'numberedList'
      ],
      shouldNotGroupWhenFull: true
    },
    balloonToolbar: [
      'bold', 'italic', '|', 'link', '|',
      'bulletedList', 'numberedList'
    ],
    fontFamily: { supportAllValues: true },
    fontSize: {
      options: [10, 12, 14, 'default', 18, 20, 22],
      supportAllValues: true
    },
    fullscreen: {
      onEnterCallback: container =>
        container.classList.add(
          'editor-container', 'editor-container_classic-editor',
          'editor-container_include-fullscreen', 'main-container'
        )
    },
    heading: {
      options: [
        { model: 'paragraph', title: 'Paragraph', class: 'ck-heading_paragraph' },
        { model: 'heading1', view: 'h1', title: 'Heading 1', class: 'ck-heading_heading1' },
        { model: 'heading2', view: 'h2', title: 'Heading 2', class: 'ck-heading_heading2' },
        { model: 'heading3', view: 'h3', title: 'Heading 3', class: 'ck-heading_heading3' },
        { model: 'heading4', view: 'h4', title: 'Heading 4', class: 'ck-heading_heading4' },
        { model: 'heading5', view: 'h5', title: 'Heading 5', class: 'ck-heading_heading5' },
        { model: 'heading6', view: 'h6', title: 'Heading 6', class: 'ck-heading_heading6' }
      ]
    },
    htmlSupport: {
      allow: [{ name: /^.*$/, styles: true, attributes: true, classes: true }]
    },
    image: {
      toolbar: [
        'toggleImageCaption', 'imageTextAlternative', '|',
        'imageStyle:inline', 'imageStyle:wrapText',
        'imageStyle:breakText', '|', 'resizeImage'
      ]
    },
    link: {
      addTargetToExternalLinks: true,
      defaultProtocol: 'https://',
      decorators: {
        toggleDownloadable: {
          mode: 'manual',
          label: 'Downloadable',
          attributes: { download: 'file' }
        }
      }
    },
    list: {
      properties: { styles: true, startIndex: true, reversed: true }
    },
    menuBar: { isVisible: true },
    placeholder: 'Type or paste your content here!',
    licenseKey: 'GPL',
    alignment: {
      options: ['left', 'center', 'right', 'justify']
    },
  }).catch(console.error);
}
