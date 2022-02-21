const { merge } = require("webpack-merge");
const baseWebpackConfig = require("./webpack.config.js");
const { CleanWebpackPlugin } = require("clean-webpack-plugin");

// const path = require("path");
// const fs = require("fs");
// const PAGES = fs
//   .readdirSync(PAGES_DIR)
//   .filter((fileName) => fileName.endsWith(".pug"));

module.exports = merge(baseWebpackConfig, {
  mode: "production",
  stats: "none",
  plugins: [
    new CleanWebpackPlugin({
      // cleanOnceBeforeBuildPatterns: [],
    }),
  ],
});
