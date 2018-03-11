const CopyWebpackPlugin = require('copy-webpack-plugin');
const ExtractTextPlugin = require('extract-text-webpack-plugin');
const SpritesmithPlugin = require('webpack-spritesmith');


module.exports = {
  entry: [
    './app/brasilgovtiles.scss',
    './app/brasilgovtiles.js',
  ],
  output: {
    filename: 'brasilgovtiles.js',
    library: 'brasilgovtiles',
    libraryExport: 'default',
    libraryTarget: 'umd',
    path: `${__dirname}/../src/brasil/gov/tiles/static`,
    pathinfo: true,
    publicPath: '++resource++brasil.gov.tiles/',
  },
  resolve: {
    extensions: ['.js'],
    modules: [
      __dirname,
      `${__dirname}/node_modules`,
    ]
  },
  module: {
    rules: [{
      test: /\.js$/,
      exclude: /(\/node_modules\/|test\.js$|\.spec\.js$)/,
      use: 'babel-loader',
    }, {
      test: /\.scss$/,
      use: ExtractTextPlugin.extract({
        fallback: 'style-loader',
        use: [
          'css-loader',
          'postcss-loader',
          'sass-loader'
        ]
      }),
    }, {
      test: /.*\.(gif|png|jpe?g)$/i,
      use: [
        {
          loader: 'file-loader',
          options: {
            name: '[path][name].[ext]',
            context: 'app/',
          }
        },
        {
          loader: 'image-webpack-loader',
          query: {
            mozjpeg: {
              progressive: true,
            },
            pngquant: {
              quality: '65-90',
              speed: 4,
            },
            gifsicle: {
              interlaced: false,
            },
            optipng: {
              optimizationLevel: 7,
            }
          }
        }
      ]
    }, {
      test: /\.svg/,
      exclude: /node_modules/,
      use: 'svg-url-loader',
    }]
  },
  devtool: 'source-map',
  plugins: [
    new CopyWebpackPlugin([{
      from: 'app/vendor/*',
      to: 'vendor',
      flatten: true
    }]),
    new ExtractTextPlugin({
      filename: 'brasilgovtiles.css',
      allChunks: true
    }),
    new SpritesmithPlugin({
      src: {
        cwd: 'app/sprite',
        glob: '*.png',
      },
      target: {
        image: 'app/img/sprite.png',
        css: 'app/scss/_sprite.scss',
      },
      apiOptions: {
        cssImageRef: './img/sprite.png',
      }
    }),
  ]
}
