const path = require('path')

module.exports = {
  devServer: {
    static: {
      directory: __dirname,
      publicPath: '/'
    }
  }
}
