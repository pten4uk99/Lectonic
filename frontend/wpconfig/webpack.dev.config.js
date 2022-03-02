const webpack = require("webpack");
const { merge } = require("webpack-merge");
const baseWebpackConfig = require("./webpack.config.js");

module.exports = merge(baseWebpackConfig, {
  mode: "development",
  devtool: "eval-source-map",
  devServer: {
    static: baseWebpackConfig.externals.paths.dist,
    port: 3000,
    hot: true,
    open: false,
    watchFiles: baseWebpackConfig.externals.paths.src,
    historyApiFallback: true,
  },
  watchOptions: {
    ignored: /node_modules/,
  },
  stats: "summary",
  plugins: [
    new webpack.SourceMapDevToolPlugin({
      filename: "[file].map",
    }),
  ],
});
