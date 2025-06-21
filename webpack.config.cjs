const path = require('path');

module.exports = {
  entry: './ckeditor5-pure.js',
  output: {
    path: path.resolve(__dirname, 'ckanext/content/assets/js/vendor'),
    filename: 'ckeditor5-bundle.js',
    library: 'CKANCKEditor5',
    libraryTarget: 'window',
  },
  module: {
    rules: [
      {
        test: /\.css$/,
        use: ['style-loader', 'css-loader', 'postcss-loader'],
      },
      {
        test: /\.svg$/,
        use: ['raw-loader'],
      }
    ]
  },
  resolve: {
    extensions: ['.js'],
  },
  mode: 'production'
};
