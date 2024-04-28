// vue.config.js
module.exports = {
  publicPath:
    process.env.NODE_ENV === "production"
      ? "/static/" // Set this to the path Django uses to serve static files
      : "/",
};
