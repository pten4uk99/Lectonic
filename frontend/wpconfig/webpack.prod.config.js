const { merge } = require("webpack-merge");
const baseWebpackConfig = require("./webpack.config.js");
const { CleanWebpackPlugin } = require("clean-webpack-plugin");

module.exports = merge(baseWebpackConfig, {
  mode: "production",
  stats: "none",
  // module: {
  //   rules: [
  //     {
  //       test: /\.(gif|png|jpe?g|svg)$/i,
  //     },
  //   ],
  // },
  // resolve: {
  //   extensions: [".gif", ".png", ".jpg", ".jpeg", ".svg"],
  // },
  plugins: [
    new CleanWebpackPlugin({
      // cleanOnceBeforeBuildPatterns: [],
    }),
  ],
});
