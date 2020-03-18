import Vue from "vue";
import { ApiConnector } from "./vstutils/api";
import { ErrorHandler } from "./vstutils/popUp";
import { guiLocalSettings } from "./vstutils/utils";

import "./app.common.js";

/**
 * Class for a App object, that will be used on api pages.
 */
export default class App {
  /**
   * Constructor of AppForApi class.
   * @param {object} api_config Dict with options for ApiConnector constructor.
   * @param {object} openapi Object with OpenAPI schema.
   * @param {object} cache Object, that manages api responses cache operations.
   */
  constructor(api_config, openapi, cache) {
    /**
     * Object, that manages connection with API (sends API requests).
     */
    this.api = new ApiConnector(api_config, openapi, cache);
    /**
     * Object, that handles errors.
     */
    this.error_handler = new ErrorHandler();
    /**
     * Array, that stores objects, containing language's name and code.
     */
    this.languages = null;
    /**
     * Dict, that stores translations for each language.
     */
    this.translations = null;
    /**
     * Object, that stores data of authorized user.
     */
    this.user = null;
  }
  /**
   * Method, that starts work of app.
   * Method gets openapi_schema, inits models, inits views and mounts application to DOM.
   */
  start() {
    let LANG = guiLocalSettings.get("lang") || "en";
    let promises = [
      this.api.getLanguages(),
      this.api.getTranslations(LANG),
      this.api.loadUser()
    ];

    return Promise.all(promises)
      .then(response => {
        this.languages = response[0];
        this.translations = {
          [LANG]: response[1]
        };
        this.user = response[2];

        fieldsRegistrator.registerAllFieldsComponents();
        this.mountApplication();
      })
      .catch(error => {
        debugger;
        throw new Error(error);
      });
  }
  /**
   * Method, that creates store and router for an application and mounts it to DOM.
   * This method creates different several Vue instances for each block of page (top_nav, side_bar and so on),
   * because if we will try to mount it to the one root '#RealBody' div, as it's done in guiApp.js,
   * we will have a bug with creating of page content (blocks with api paths), generated by Swagger JS scripts.
   */
  mountApplication() {
    tabSignal.emit("app.beforeInit", { app: this });

    function setOriginalLinks(menu, host) {
      for (let index = 0; index < menu.length; index++) {
        let item = menu[index];

        if (item.url) {
          item.origin_link = true;
          item.url = host + "/#" + item.url;
        }

        if (item.sublinks) {
          item.sublinks = setOriginalLinks(item.sublinks, host);
        }
      }

      return menu;
    }

    let i18n = new VueI18n({
      locale: guiLocalSettings.get("lang") || "en",
      messages: this.translations
    });

    let x_menu = setOriginalLinks(
      [...app.api.openapi.info["x-menu"]],
      this.api.getHostUrl()
    );

    this.top_nav = new Vue({
      data: {
        a_links: true
      },
      i18n: i18n
    }).$mount("#top_nav_wrapper");

    this.sidebar = new Vue({
      data: {
        info: app.api.openapi.info,
        x_menu: x_menu,
        x_docs: app.api.openapi.info["x-docs"],
        a_links: true
      },
      i18n: i18n
    }).$mount("#sidebar_wrapper");

    this.gui_customizer = new Vue({ i18n: i18n }).$mount(
      "#gui_customizer_wrapper"
    );

    this.footer = new Vue({ i18n: i18n }).$mount("#main_footer_wrapper");

    tabSignal.emit("app.afterInit", { app: this });
  }
}

window.App = App;