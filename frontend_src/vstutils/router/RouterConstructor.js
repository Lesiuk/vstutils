import VueRouter from 'vue-router';
import { signals } from '../../libs/TabSignal.js';

/**
 * Class, that manages Router creation.
 * In current realization, Router is Vue-Router.
 * More about Vue-Router - https://router.vuejs.org/.
 */
export default class RouterConstructor {
    /**
     * Constructor of RouterConstructor Class.
     * @param {object} views Dict with views objects.
     * @param {object} components_templates Dict with mixins for Vue components of Views,
     * generated by View class and having description in OpenAPI Schema.
     * @param {object} custom_components_templates Dict with mixins for Vue components
     * of custom Views, that have no description in OpenAPI Schema (home page, 404 error page).
     */
    constructor(views, components_templates, custom_components_templates) {
        this.views = views;
        this.components_templates = components_templates;
        this.custom_components_templates = custom_components_templates;
        this.routes = [];
    }

    /**
     * Method, that returns mixin for Vue component for a route, connected with current view.
     * @param {object} view JS object, with options for a current view.
     * @return {object} Vue Component for a Route.
     */
    getRouteComponent(view) {
        return {
            mixins: this.getRouteComponentMixins(view),
            template: view.template,
            data: function () {
                return {
                    view: view,
                };
            },
        };
    }

    /**
     * Method, that collects appropriate mixins for a view Vue component into one array.
     * @param {object} view JS object, with options for a current view.
     * @return {array} Mixins Array for a Vue component.
     */
    getRouteComponentMixins(view) {
        return [this.components_templates.base, this.components_templates[view.schema.type]].concat(
            view.mixins || [],
        );
    }

    /**
     * Method, that returns array of routes objects, existing in current App.
     * @return {array} Routes Array.
     */
    getRoutes() {
        this.routes = this.formAllRoutes();
        return this.routes;
    }

    /**
     * Method, that forms array of all routes objects, existing in current App.
     * @return {array} Routes Array.
     */
    formAllRoutes() {
        let routes = [
            {
                name: 'home',
                path: '/',
                component: this.custom_components_templates.home || {},
            },
        ];

        this.emitSignalAboutRouteCreation(routes.last);

        routes = routes.concat(this.formRoutesBasedOnViews(), this.formRoutesBasedOnCustomComponents(), {
            name: '404',
            path: '*',
            component: this.custom_components_templates['404'] || {},
        });

        this.emitSignalAboutRouteCreation(routes.last);

        signals.emit('allRoutes.created', routes);

        return routes;
    }

    /**
     * Method, that forms array of routes objects, existing in current App, and based on App Views, that have description in OpenAPI Schema (this.views).
     * @return {array} Routes Array.
     */
    formRoutesBasedOnViews() {
        let routes = [];

        for (let path in this.views) {
            if (!Object.prototype.hasOwnProperty.call(this.views, path)) {
                continue;
            }

            routes.push({
                name: path,
                path: this.views[path].getPathTemplateForRouter(path),
                component: this.getRouteComponent(this.views[path]),
            });

            this.emitSignalAboutRouteCreation(routes.last);
        }

        return routes;
    }

    /**
     * Method, that forms array of possible routes of App based on App custom views components
     * (this.custom_components_templates).
     * @return {array} Routes Array.
     */
    formRoutesBasedOnCustomComponents() {
        let routes = [];

        for (let item in this.custom_components_templates) {
            if (!Object.prototype.hasOwnProperty.call(this.custom_components_templates, item)) {
                continue;
            }

            if (['home', '404'].includes(item)) {
                continue;
            }

            let path_template = item.replace(/{/g, ':').replace(/}/g, '');

            if (
                this.custom_components_templates[item].getPathTemplateForRouter &&
                typeof this.custom_components_templates[item].getPathTemplateForRouter === 'function'
            ) {
                path_template = this.custom_components_templates[item].getPathTemplateForRouter(item);
            }

            routes.push({
                name: item,
                path: path_template,
                component: this.custom_components_templates[item],
            });

            this.emitSignalAboutRouteCreation(routes.last);
        }

        return routes;
    }

    /**
     * Method emits signal: "route was created".
     * @param {object} route Object with route properties (name, path, component).
     */
    emitSignalAboutRouteCreation(route) {
        signals.emit('routes[' + route.name + '].created', route);
    }

    /**
     * Method, that returns new instance of VueRouter.
     * @return {object} VueRouter.
     */
    getRouter() {
        return new VueRouter({
            routes: this.getRoutes(),
        });
    }
}
