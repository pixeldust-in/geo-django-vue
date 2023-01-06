const { defineConfig } = require('@vue/cli-service')

let BundleTracker = require("webpack-bundle-tracker");
const path = require("path");

const STATIC_URL = "/assets/";
const PORT = process.env.PORT || 3000;


const BASE_URL = {
  production: `${STATIC_URL}app-build`,
  development: `http://localhost:${PORT}/`,

};

module.exports = defineConfig({
  transpileDependencies: true,
  publicPath: BASE_URL[process.env.NODE_ENV] || BASE_URL.production,
  outputDir: path.resolve(__dirname, "../assets/app-build"),
  devServer: {
      port: PORT,
      allowedHosts: "all",
      headers: { "Access-Control-Allow-Origin": "*" },
    },
    configureWebpack: config => {
      config.plugins.push(new BundleTracker());
    }
})



// module.exports = {
//   transpileDependencies: true,

//
//
//
// }
