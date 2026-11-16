"use strict";

function _typeof(obj) { "@babel/helpers - typeof"; return _typeof = "function" == typeof Symbol && "symbol" == typeof Symbol.iterator ? function (obj) { return typeof obj; } : function (obj) { return obj && "function" == typeof Symbol && obj.constructor === Symbol && obj !== Symbol.prototype ? "symbol" : typeof obj; }, _typeof(obj); }
/* eslint no-use-before-define: ["error", "nofunc"] */

// @ts-check

/**
 * Developer note:
 * Run the following command to turn JS-template into handlebars-file:
 *    babel webformloader.template.js -o webformloaderjs.handlebars --no-babelrc --presets=@babel/preset-env
 */

/**
 * This script is made accessible as "https://www.kth.se/form/webform/niseko/webformloader.js".
 *
 * It can be used to embed a Niseko-form with a given ID (e.g. "567890123456789012345678")
 * on a web-page which is hosted at a known server (search for Global.allowedOrigins, here).
 *
 * The hosting web-page should include HTML-code like this:
 *   <script src="http://www.kth.se/form/webform/niseko/webformloader.js" type="text/javascript"></script>
 *   <span id="567890123456789012345678"></span>
 *   <script type="text/javascript">
 *     window.addEventListener('load', function () {
 *       var options = {};
 *       options.tags = [];
 *       // options.tags = [{ name: 'tagName1', value: 'value1' }, { name: 'tagName2', value: 'value2' }];
 *       // options.cssUrl = 'http://www.../other.css';
 *       options.host = 'https://www.kth.se';
 *       getEmbeddedForm("567890123456789012345678", options);
 *     }, { once: true });
 *   </script>
 *
 * The function "getEmbeddedForm()" will do the following:
 * - It puts a new iFrame into the prepared <span id="...">-element
 *   which will be filled with the Niseko-form matching the given ID.
 * - It installs a listener to "message"-events: The embedded form will use "window.parent.postMessage()"
 *   to signalize any resize of the form to the hosting web-page and the web-page will then change
 *   the iFrame's height accordingly. (The code to send messages can be found in "embed.jsx"...)
 */

// Updated for react niseko form

installWebformLoader();
function installWebformLoader() {
  // eslint-disable-next-line prefer-const
  var handlebarsInput = {};
  /* **/ handlebarsInput = { webformUrl: 'https://www.kth.se/form/embed/:id', debug: true } /** */
  var QUERY_WEBFORM_ROUTE = handlebarsInput.webformUrl == null ? 'http://localhost:3000/form/embed/:id' : handlebarsInput.webformUrl;
  var DEBUG = handlebarsInput.debug == null ? false : handlebarsInput.debug;
  var Global = {
    options: {},
    myId: null,
    myIFrameId: null,
    targetOrigin: '*',
    allowedOrigins: ['*']
  };
  debug('FormLoader - Initializing...');
  window.addEventListener('message', handleMsgFromIFrame);

  // @ts-ignore
  window.getEmbeddedForm = getEmbeddedForm;

  // @ts-ignore
  // eslint-disable-next-line no-undef
  var hasJQueryToo = typeof $ === 'function' && $.fn != null && _typeof($.fn) === 'object';
  if (hasJQueryToo) {
    debug('FormLoader - Found jQuery, adding support...');
    // @ts-ignore
    // eslint-disable-next-line no-undef
    $.fn.niseko = function addDeprecatedJQuerySupport(conf) {
      debug('WARNING: FormLoader - jQuery support is deprecated, please switch to getEmbeddedForm(id, options)');
      // @ts-ignore
      // eslint-disable-next-line no-undef
      getEmbeddedForm($(this).attr('id'), conf);
    };
  }
  function debug(message) {
    if (DEBUG && console) {
      // eslint-disable-next-line no-console
      console.log(message);
    }
  }

  /**
   * Looks for the right <span id="..."></span> and adds the webform as an iFrame.
   *
   * @param {string} formId Database ID of the Niseko form
   * @param {object} [conf]
   * @param {object[]} conf.tags e.g. [{ name: 'tagName1', value: 'value1' }]
   * @param {string} conf.host e.g. 'https://www.kth.se'
   * @param {string} conf.cssUrl something like 'http://www.../other.css'
   */
  function getEmbeddedForm(formId, conf) {
    var gotConfiguration = conf != null && _typeof(conf) === 'object';
    Global.options = {
      height: 0,
      tags: gotConfiguration && Array.isArray(conf.tags) ? conf.tags : [],
      host: gotConfiguration && typeof conf.host === 'string' && conf.host !== '' ? conf.host : null,
      cssUrl: gotConfiguration && typeof conf.cssUrl === 'string' && conf.cssUrl !== '' ? conf.cssUrl : null
    };
    Global.allowedOrigins = ['https://www.kth.se', 'https://intra.kth.se', 'https://www-r.referens.sys.kth.se', 'https://app-r.referens.sys.kth.se', 'http://localhost:3000'];
    if (Global.options.host) {
      Global.targetOrigin = Global.options.host;
    }
    if (formId) {
      Global.myId = formId;
      Global.myIFrameId = getIFrameId(formId);
    }
    debug('myId: ' + Global.myId);
    debug('iFrameId: ' + Global.myIFrameId);
    if (Global.myId) {
      addIFrame();
    }
  }
  function handleMsgFromIFrame(event) {
    var originIsValid = Global.allowedOrigins.some(function (item) {
      return item === event.origin || item === '*';
    });
    if (!originIsValid || event == null || _typeof(event) !== 'object' || !event.data) {
      return;
    }
    var message = null;
    try {
      message = JSON.parse(event.data);
    } catch (error) {
      console.log(error);
      return;
    }
    if (message == null || _typeof(message) !== 'object') {
      return;
    }
    var content = message.message;
    // if (content === 'Pretty Polly!') {
    //   const aMessage = { name: Global.options.name }
    //   sendMsgToIFrame('info', aMessage, event)
    // }

    if (content != null && _typeof(content) === 'object' && content.frameId && content.height) {
      debug('FormLoader::handleMsgFromIFrame: resize iframe');
      resizeIFrameElement(content.frameId, content.height, content.doScroll);
    }
  }

  /**
   * Resizes the iframe with a specified id to dynamicly
   * fit the underlying iframe document height.
   */
  function resizeIFrameElement(_id, height) {
    var doScroll = arguments.length > 2 && arguments[2] !== undefined ? arguments[2] : false;
    debug('Resizing iFrame height for ' + _id + ' to ' + height + ' doScroll = ' + doScroll);
    var iframe = document.getElementById(getIFrameId(_id));
    iframe.setAttribute('height', height);
    if (doScroll) {
      var yOffset = 0;
      if (document.querySelector('.use-personal-menu')) {
        yOffset = -33;
      }
      var y = iframe.getBoundingClientRect().top + window.pageYOffset + yOffset;
      window.scrollTo({
        top: y,
        behavior: 'smooth'
      });
    }
  }

  /**
  function sendMsgToIFrame(messageType, messageData, event) {
    const _targetOrigin = event ? event.origin : Global.targetOrigin
     const data = { type: messageType }
    if (messageType === 'tags') {
      data.tags = messageData
    } else {
      data.message = messageData
    }
     debug('FormLoader - Sending Event to[' + _targetOrigin + ' - ]: ' + JSON.stringify(data))
     const iFrameElement = document.getElementById(Global.myIFrameId)
    if (!iFrameElement || iFrameElement.tagName !== 'IFRAME') {
      debug("FormLoader::sendMsgToIFrame - Unexpected error: Can't find IFrame")
      return
    }
     // @ts-ignore
    const iFrameWindow = iFrameElement.contentWindow
    iFrameWindow.postMessage(JSON.stringify(data), '*')
    debug('sendMessage(FormLoader) - Sending event')
  }
  */

  /**
   * @param {string} _id
   */
  function getIFrameId(_id) {
    return 'iframe-' + _id;
  }

  /**
   * Adds the iFrame that displays the webform to the user.
   */
  function addIFrame() {
    // eslint-disable-next-line no-console
    console.log('Adding iFrame to the page with an ID-attribute matching _id...');
    var uri = getWebformUrl();
    var iframe = document.createElement('IFRAME');
    iframe.setAttribute('title', 'form');
    iframe.setAttribute('id', Global.myIFrameId);
    iframe.setAttribute('src', uri);
    iframe.setAttribute('frameborder', '0');
    iframe.setAttribute('width', '100%');
    iframe.setAttribute('height', String(Global.options.height));
    iframe.setAttribute('scrolling', 'no');
    iframe.setAttribute('allowtransparency', 'true');
    // iframe.setAttribute('style', 'outline: none')
    // const resizeMightCauseProblemsInChrome2020 = container.tagName.toUpperCase() === 'SPAN'
    // if (resizeMightCauseProblemsInChrome2020) {
    //   const divContainer = document.createElement('DIV')
    //   divContainer.setAttribute('id', Global.myId)
    //   divContainer.setAttribute('data-original-tagname', 'span')
    //   container.parentNode.replaceChild(divContainer, container)
    //   container = divContainer
    // }
    document.getElementById(Global.myId).appendChild(iframe);
    debug('ID in addIFrame: ' + Global.myIFrameId);
  }

  /**
   * @returns {string} URL which will be used to include webform
   */
  function getWebformUrl() {
    var urlWithoutQueryParameters = QUERY_WEBFORM_ROUTE.replace(':id', Global.myId);
    var queryParameters = [];
    queryParameters.push('caller=' + encodeURIComponent(JSON.stringify({
      url: document.URL
    })));
    if (Global.options.tags) {
      queryParameters.push('tags=' + encodeURIComponent(JSON.stringify(Global.options.tags)));
    }
    if (Global.options.cssUrl) {
      queryParameters.push('css=' + encodeURIComponent(Global.options.cssUrl));
    }
    var url = queryParameters.length > 0 ? urlWithoutQueryParameters + '?' + queryParameters.join('&') : urlWithoutQueryParameters;
    debug('The webform to load in the iFrame is ' + url);
    return url;
  }
}