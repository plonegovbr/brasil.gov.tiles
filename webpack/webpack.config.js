const makeConfig = require('sc-recipe-staticresources');
const CopyWebpackPlugin = require('copy-webpack-plugin');


module.exports = makeConfig(
  // name
  'brasil.gov.tiles',

  // shortName
  'brasilgovtiles',

  // path
  `${__dirname}/../src/brasil/gov/tiles/browser/static`,

  //publicPath
  '++resource++brasil.gov.tiles/',

  //callback
  function(config, options) {
    config.plugins.push(
      new CopyWebpackPlugin([{
        from: 'app/vendor/*',
        to: 'vendor',
        flatten: true
      }]),
    );
  },
);
