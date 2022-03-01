const MiniCssExtractPlugin = require('mini-css-extract-plugin')
const HtmlWebpackPlugin = require('html-webpack-plugin')
const TerserWebpackPlugin = require('terser-webpack-plugin')
const CssMinimizerPlugin = require('css-minimizer-webpack-plugin')
const StylelintPlugin = require('stylelint-webpack-plugin')
const CopyWebpackPlugin = require('copy-webpack-plugin')

const path = require('path')
const fs = require('fs')

const PATHS = {
  src: path.join(__dirname, '../src/'),
  public: path.join(__dirname, '../public/'),
  build: path.join(__dirname, '../build/'),
  conf: path.join(__dirname, './'),
  assets: 'assets/',
}

const PAGES_DIR = `${PATHS.src}/pages/`

module.exports = {
  externals: {
    paths: PATHS,
  },
  entry: {
    app: `${PATHS.src}index.jsx`,
  },
  output: {
    filename: 'js/[name].[chunkhash].js',
    path: PATHS.build,
  },
  optimization: {
    splitChunks: {
      cacheGroups: {
        vendor: {
          name: 'vendors',
          test: /node_modules/,
          chunks: 'all',
          enforce: true,
        },
      },
    },
  },
  module: {
    rules: [
      {
        test: /\.(js|jsx)$/,
        exclude: /node_modules/,
        use: ['babel-loader'],
      },
      {
        test: /\.css$/,
        use: [
          {
            loader: MiniCssExtractPlugin.loader,
            options: {
              publicPath: `${PATHS.assets}css/`,
              esModule: true,
            },
          },
          'css-loader',
          {
            loader: 'postcss-loader',
            options: {
              postcssOptions: {
                config: `${PATHS.conf}/postcss.config.js`,
              },
            },
          },
        ],
      },
      {
        test: /\.scss$/,
        use: [
          {
            loader: MiniCssExtractPlugin.loader,
            options: {
              esModule: true,
            },
          },
          {
            loader: 'postcss-loader',
            options: {
              postcssOptions: {
                config: `${PATHS.conf}/postcss.config.js`,
              },
            },
          },
          'css-loader',
          'sass-loader',
        ],
      },
      {
        test: /\.styl$/,
        use: [
          MiniCssExtractPlugin.loader,
          {
            loader: 'css-loader',
            options: {
              sourceMap: true,
              esModule: true,
            },
          },
          {
            loader: 'postcss-loader',
            options: {
              sourceMap: true,
              postcssOptions: {
                config: `${PATHS.conf}/postcss.config.js`,
              },
            },
          },
          {
            loader: 'stylus-loader',
            options: { sourceMap: true },
          },
        ],
      },

      {
        test: /\.(gif|png|jpe?g|svg)$/i,
        loader: 'file-loader',
        options: {
          outputPath: PATHS.assets + 'img',
          name: '[name].[ext]',
        },
      },
      {
        test: /\.(woff(2)?|ttf|eot)$/i,
        loader: 'file-loader',
        options: {
          outputPath: PATHS.assets + 'fonts',
          name: '[name].[ext]',
        },
      },
    ],
  },
  resolve: {
    alias: {
      '~': path.resolve(__dirname, '../src/'),
      '~@': path.resolve(__dirname, '../src/components/'),
    },
    extensions: ['', '.js', '.jsx'],
  },
  plugins: [
    new MiniCssExtractPlugin({
      filename: `css/[name].[contenthash].css`,
    }),
    new CopyWebpackPlugin({
      patterns: [
        { from: `${PATHS.src}/${PATHS.assets}img`, to: `${PATHS.assets}img` },
        {
          from: `${PATHS.src}/${PATHS.assets}fonts`,
          to: `${PATHS.assets}fonts`,
        },
        { from: `${PATHS.src}/static`, to: '' },
      ],
    }),
    new TerserWebpackPlugin(),
    new CssMinimizerPlugin(),
    // new StylelintPlugin(),
    new HtmlWebpackPlugin({ template: `${PAGES_DIR}index.html` }),
  ],
  optimization: {
    minimizer: [new TerserWebpackPlugin({}), new CssMinimizerPlugin({})],
  },
}
