
(function (global, factory) {
    typeof exports === 'object' && typeof module !== 'undefined' ? factory(exports) :
    typeof define === 'function' && define.amd ? define(['exports'], factory) :
    (global = global || self, factory(global.fontawesome = {}));
  }(this, (function (exports) { 'use strict';
  
    var _WINDOW = {};
    var _DOCUMENT = {};
  
    try {
      if (typeof window !== 'undefined') _WINDOW = window;
      if (typeof document !== 'undefined') _DOCUMENT = document;
    } catch (e) {}
  
    var _ref = _WINDOW.navigator || {},
        _ref$userAgent = _ref.userAgent,
        userAgent = _ref$userAgent === void 0 ? '' : _ref$userAgent;
  
    var WINDOW = _WINDOW;
    var DOCUMENT = _DOCUMENT;
    var IS_BROWSER = !!WINDOW.document;
    var IS_DOM = !!DOCUMENT.documentElement && !!DOCUMENT.head && typeof DOCUMENT.addEventListener === 'function' && typeof DOCUMENT.createElement === 'function';
    var IS_IE = ~userAgent.indexOf('MSIE') || ~userAgent.indexOf('Trident/');
  
    function ownKeys(object, enumerableOnly) {
      var keys = Object.keys(object);
  
      if (Object.getOwnPropertySymbols) {
        var symbols = Object.getOwnPropertySymbols(object);
        enumerableOnly && (symbols = symbols.filter(function (sym) {
          return Object.getOwnPropertyDescriptor(object, sym).enumerable;
        })), keys.push.apply(keys, symbols);
      }
  
      return keys;
    }
  
    function _objectSpread2(target) {
      for (var i = 1; i < arguments.length; i++) {
        var source = null != arguments[i] ? arguments[i] : {};
        i % 2 ? ownKeys(Object(source), !0).forEach(function (key) {
          _defineProperty(target, key, source[key]);
        }) : Object.getOwnPropertyDescriptors ? Object.defineProperties(target, Object.getOwnPropertyDescriptors(source)) : ownKeys(Object(source)).forEach(function (key) {
          Object.defineProperty(target, key, Object.getOwnPropertyDescriptor(source, key));
        });
      }
  
      return target;
    }
  
    function _defineProperty(obj, key, value) {
      if (key in obj) {
        Object.defineProperty(obj, key, {
          value: value,
          enumerable: true,
          configurable: true,
          writable: true
        });
      } else {
        obj[key] = value;
      }
  
      return obj;
    }
  
    // Simplified version of icon management and rendering
    function icon(iconDefinition) {
      if (iconDefinition && iconDefinition.prefix && iconDefinition.iconName) {
        return {
          html: `<svg class="svg-inline--fa" aria-hidden="true" focusable="false" role="img" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${iconDefinition.width} ${iconDefinition.height}">
            <path fill="currentColor" d="${iconDefinition.svgPathData}"></path>
          </svg>`
        };
      }
      return null;
    }
  
    // Basic icon replacement function
    function replace(mutation) {
      if (!IS_DOM) return;
  
      try {
        var elements = DOCUMENT.querySelectorAll('.fa, .fab, .fas, .far, .fal, .fad');
        
        elements.forEach(function (el) {
          if (el.classList.contains('fa-replace')) return;
  
          var prefix = el.getAttribute('data-prefix') || 'fas';
          var iconName = el.getAttribute('data-icon') || '';
  
          if (prefix && iconName) {
            var iconData = {
              prefix: prefix,
              iconName: iconName,
              width: 512,  // Default width
              height: 512, // Default height
              svgPathData: '' // Placeholder for SVG path
            };
  
            var iconHtml = icon(iconData);
            if (iconHtml) {
              el.innerHTML = iconHtml.html;
              el.classList.add('fa-replace');
            }
          }
        });
      } catch (e) {
        console.error('Font Awesome icon replacement error:', e);
      }
    }
  
    // Mutation observer to handle dynamic content
    function observe() {
      if (!IS_DOM) return;
  
      var observer = new MutationObserver(function (mutations) {
        mutations.forEach(function () {
          replace();
        });
      });
  
      observer.observe(DOCUMENT.body, {
        childList: true,
        subtree: true
      });
    }
  
    // Public API
    var api = {
      icon: icon,
      replace: replace,
      observe: observe
    };
  
    // Auto-replace on load
    if (IS_DOM) {
      WINDOW.FontAwesome = api;
      
      // Initial icon replacement
      replace();
      
      // Start observing for dynamic content changes
      observe();
    }
  
    exports.icon = icon;
    exports.replace = replace;
    exports.observe = observe;
    exports.default = api;
  
    Object.defineProperty(exports, '__esModule', { value: true });
  
  })));