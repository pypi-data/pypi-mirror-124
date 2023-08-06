"use strict";
(self["webpackChunk_educational_technology_collective_etc_jupyterlab_telemetry_library"] = self["webpackChunk_educational_technology_collective_etc_jupyterlab_telemetry_library"] || []).push([["lib_index_js"],{

/***/ "./lib/config_supplicant.js":
/*!**********************************!*\
  !*** ./lib/config_supplicant.js ***!
  \**********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "ConfigSupplicant": () => (/* binding */ ConfigSupplicant)
/* harmony export */ });
class ConfigSupplicant {
    constructor({ paths, config }) {
        this.enable = this.enable.bind(this);
        this.disable = this.disable.bind(this);
        this.init = this.init.bind(this);
        this._config = config;
        this._paths = paths;
    }
    init() {
        try {
            let state = this._paths.reduce((previousValue, currentValue) => {
                return previousValue[currentValue];
            }, this._config);
            //  We need to know the value assigned to the reference path (i.e., paths); 
            //  hence, drill into the arbitrary config object in order to obtain the value.    
            if (state === false) {
                this.disable();
            }
            else if (state === true) {
                this.enable();
            }
            else {
                throw new Error();
            }
        }
        catch (e) {
            this.enable();
            //  The default is for all events to be enabled; hence, we don't need to log anything here.
        }
    }
}


/***/ }),

/***/ "./lib/events.js":
/*!***********************!*\
  !*** ./lib/events.js ***!
  \***********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "NotebookSaveEvent": () => (/* binding */ NotebookSaveEvent),
/* harmony export */   "CellExecutionEvent": () => (/* binding */ CellExecutionEvent),
/* harmony export */   "NotebookScrollEvent": () => (/* binding */ NotebookScrollEvent),
/* harmony export */   "ActiveCellChangeEvent": () => (/* binding */ ActiveCellChangeEvent),
/* harmony export */   "NotebookOpenEvent": () => (/* binding */ NotebookOpenEvent),
/* harmony export */   "CellAddEvent": () => (/* binding */ CellAddEvent),
/* harmony export */   "CellRemoveEvent": () => (/* binding */ CellRemoveEvent),
/* harmony export */   "CellErrorEvent": () => (/* binding */ CellErrorEvent)
/* harmony export */ });
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @lumino/signaling */ "webpack/sharing/consume/default/@lumino/signaling");
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_lumino_signaling__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _config_supplicant__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./config_supplicant */ "./lib/config_supplicant.js");



class NotebookSaveEvent extends _config_supplicant__WEBPACK_IMPORTED_MODULE_2__.ConfigSupplicant {
    constructor({ notebookPanel, config }) {
        super({
            paths: ["mentoracademy.org/schemas/events/1.0.0/NotebookSaveEvent", "enable"],
            config
        });
        this._notebookSaved = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_1__.Signal(this);
        this._notebookPanel = notebookPanel;
        notebookPanel.disposed.connect(this.dispose, this);
        this.init();
    }
    dispose() {
        _lumino_signaling__WEBPACK_IMPORTED_MODULE_1__.Signal.disconnectAll(this);
    }
    event(context, saveState) {
        let cell;
        let cells;
        let index;
        if (saveState.match("completed")) {
            cells = [];
            for (index = 0; index < this._notebookPanel.content.widgets.length; index++) {
                cell = this._notebookPanel.content.widgets[index];
                if (this._notebookPanel.content.isSelectedOrActive(cell)) {
                    cells.push({ id: cell.model.id, index });
                }
            }
            this._notebookSaved.emit({
                event_name: "save_notebook",
                cells: cells,
                notebookPanel: this._notebookPanel
            });
        }
    }
    enable() {
        (async () => {
            await this._notebookPanel.revealed;
            this._notebookPanel.context.saveState.connect(this.event, this);
        })();
    }
    disable() {
        this._notebookPanel.context.saveState.disconnect(this.event, this);
    }
    get notebookSaved() {
        return this._notebookSaved;
    }
}
class CellExecutionEvent extends _config_supplicant__WEBPACK_IMPORTED_MODULE_2__.ConfigSupplicant {
    constructor({ notebookPanel, config }) {
        super({
            paths: ["mentoracademy.org/schemas/events/1.0.0/CellExecutionEvent", "enable"],
            config
        });
        this._cellExecuted = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_1__.Signal(this);
        this._notebookPanel = notebookPanel;
        this._notebook = notebookPanel.content;
        notebookPanel.disposed.connect(this.dispose, this);
        this.init();
    }
    dispose() {
        _lumino_signaling__WEBPACK_IMPORTED_MODULE_1__.Signal.disconnectAll(this);
    }
    event(_, args) {
        if (args.notebook.model === this._notebook.model) {
            let cells = [
                {
                    id: args.cell.model.id,
                    index: this._notebook.widgets.findIndex((value) => value == args.cell)
                }
            ];
            this._cellExecuted.emit({
                event_name: "cell_executed",
                cells: cells,
                notebookPanel: this._notebookPanel
            });
        }
    }
    enable() {
        (async () => {
            await this._notebookPanel.revealed;
            _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__.NotebookActions.executed.connect(this.event, this);
        })();
    }
    disable() {
        _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__.NotebookActions.executed.disconnect(this.event, this);
    }
    get cellExecuted() {
        return this._cellExecuted;
    }
}
class NotebookScrollEvent extends _config_supplicant__WEBPACK_IMPORTED_MODULE_2__.ConfigSupplicant {
    constructor({ notebookPanel, config }) {
        super({
            paths: ["mentoracademy.org/schemas/events/1.0.0/NotebookScrollEvent", "enable"],
            config
        });
        this._notebookScrolled = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_1__.Signal(this);
        this._notebookPanel = notebookPanel;
        this._notebook = notebookPanel.content;
        this._timeout = 0;
        this.event = this.event.bind(this);
        notebookPanel.disposed.connect(this.dispose, this);
        this.init();
    }
    dispose() {
        _lumino_signaling__WEBPACK_IMPORTED_MODULE_1__.Signal.disconnectAll(this);
    }
    event(e) {
        e.stopPropagation();
        clearTimeout(this._timeout);
        this._timeout = setTimeout(() => {
            let cells = [];
            let cell;
            let index;
            let id;
            for (index = 0; index < this._notebook.widgets.length; index++) {
                cell = this._notebook.widgets[index];
                let cellTop = cell.node.offsetTop;
                let cellBottom = cell.node.offsetTop + cell.node.offsetHeight;
                let viewTop = this._notebook.node.scrollTop;
                let viewBottom = this._notebook.node.scrollTop + this._notebook.node.clientHeight;
                if (cellTop > viewBottom || cellBottom < viewTop) {
                    continue;
                }
                id = cell.model.id;
                cells.push({ id, index });
            }
            this._notebookScrolled.emit({
                event_name: "scroll",
                cells: cells,
                notebookPanel: this._notebookPanel
            });
        }, 1000);
    }
    enable() {
        (async () => {
            await this._notebookPanel.revealed;
            this._notebook.node.addEventListener("scroll", this.event, false);
        })();
    }
    disable() {
        this._notebook.node.removeEventListener("scroll", this.event, false);
    }
    get notebookScrolled() {
        return this._notebookScrolled;
    }
}
class ActiveCellChangeEvent extends _config_supplicant__WEBPACK_IMPORTED_MODULE_2__.ConfigSupplicant {
    constructor({ notebookPanel, config }) {
        super({
            paths: ["mentoracademy.org/schemas/events/1.0.0/ActiveCellChangeEvent", "enable"],
            config
        });
        this._activeCellChanged = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_1__.Signal(this);
        this._notebookPanel = notebookPanel;
        this._notebook = notebookPanel.content;
        notebookPanel.disposed.connect(this.dispose, this);
        this.init();
    }
    dispose() {
        _lumino_signaling__WEBPACK_IMPORTED_MODULE_1__.Signal.disconnectAll(this);
    }
    event(send, args) {
        let cells = [
            {
                id: args.model.id,
                index: this._notebook.widgets.findIndex((value) => value == args)
            }
        ];
        this._activeCellChanged.emit({
            event_name: "active_cell_changed",
            cells: cells,
            notebookPanel: this._notebookPanel
        });
    }
    enable() {
        (async () => {
            await this._notebookPanel.revealed;
            this._notebook.activeCellChanged.connect(this.event, this);
        })();
    }
    disable() {
        this._notebook.activeCellChanged.disconnect(this.event, this);
    }
    get activeCellChanged() {
        return this._activeCellChanged;
    }
}
class NotebookOpenEvent extends _config_supplicant__WEBPACK_IMPORTED_MODULE_2__.ConfigSupplicant {
    constructor({ notebookPanel, config }) {
        super({
            paths: ["mentoracademy.org/schemas/events/1.0.0/NotebookOpenEvent", "enable"],
            config
        });
        this._notebookOpened = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_1__.Signal(this);
        this._once = false;
        this._notebookPanel = notebookPanel;
        this._notebook = notebookPanel.content;
        notebookPanel.disposed.connect(this.dispose, this);
        this.init();
    }
    dispose() {
        _lumino_signaling__WEBPACK_IMPORTED_MODULE_1__.Signal.disconnectAll(this);
    }
    event() {
        let cells = this._notebook.widgets.map((cell, index) => ({ id: cell.model.id, index: index }));
        this._notebookOpened.emit({
            event_name: "open_notebook",
            cells: cells,
            notebookPanel: this._notebookPanel
        });
        this._once = true;
    }
    enable() {
        if (!this._once) {
            (async () => {
                await this._notebookPanel.revealed;
                this.event();
            })();
        }
    }
    disable() {
        return;
    }
    get notebookOpened() {
        return this._notebookOpened;
    }
}
class CellAddEvent extends _config_supplicant__WEBPACK_IMPORTED_MODULE_2__.ConfigSupplicant {
    constructor({ notebookPanel, config }) {
        super({
            paths: ["mentoracademy.org/schemas/events/1.0.0/CellAddEvent", "enable"],
            config
        });
        this._cellAdded = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_1__.Signal(this);
        this._notebookPanel = notebookPanel;
        this._notebook = notebookPanel.content;
        notebookPanel.disposed.connect(this.dispose, this);
        this.init();
    }
    dispose() {
        _lumino_signaling__WEBPACK_IMPORTED_MODULE_1__.Signal.disconnectAll(this);
    }
    event(sender, args) {
        if (args.type == "add") {
            let cells = [{ id: args.newValues[0].id, index: args.newIndex }];
            this._cellAdded.emit({
                event_name: "add_cell",
                cells: cells,
                notebookPanel: this._notebookPanel
            });
        }
    }
    enable() {
        (async () => {
            var _a;
            await this._notebookPanel.revealed;
            (_a = this._notebook.model) === null || _a === void 0 ? void 0 : _a.cells.changed.connect(this.event, this);
        })();
    }
    disable() {
        var _a;
        (_a = this._notebook.model) === null || _a === void 0 ? void 0 : _a.cells.changed.disconnect(this.event, this);
    }
    get cellAdded() {
        return this._cellAdded;
    }
}
class CellRemoveEvent extends _config_supplicant__WEBPACK_IMPORTED_MODULE_2__.ConfigSupplicant {
    constructor({ notebookPanel, config }) {
        super({
            paths: ["mentoracademy.org/schemas/events/1.0.0/CellRemoveEvent", "enable"],
            config
        });
        this._cellRemoved = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_1__.Signal(this);
        this._notebookPanel = notebookPanel;
        this._notebook = notebookPanel.content;
        notebookPanel.disposed.connect(this.dispose, this);
        this.init();
    }
    dispose() {
        _lumino_signaling__WEBPACK_IMPORTED_MODULE_1__.Signal.disconnectAll(this);
    }
    event(sender, args) {
        if (args.type == "remove") {
            let cells = [{ id: args.oldValues[0].id, index: args.oldIndex }];
            this._cellRemoved.emit({
                event_name: "remove_cell",
                cells: cells,
                notebookPanel: this._notebookPanel
            });
        }
    }
    enable() {
        (async () => {
            var _a;
            await this._notebookPanel.revealed;
            (_a = this._notebook.model) === null || _a === void 0 ? void 0 : _a.cells.changed.connect(this.event, this);
        })();
    }
    disable() {
        var _a;
        (_a = this._notebook.model) === null || _a === void 0 ? void 0 : _a.cells.changed.disconnect(this.event, this);
    }
    get cellRemoved() {
        return this._cellRemoved;
    }
}
class CellErrorEvent extends _config_supplicant__WEBPACK_IMPORTED_MODULE_2__.ConfigSupplicant {
    constructor({ notebookPanel, config }) {
        super({
            paths: ["mentoracademy.org/schemas/events/1.0.0/CellErrorEvent", "enable"],
            config
        });
        this._cellErrored = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_1__.Signal(this);
        this._notebookPanel = notebookPanel;
        notebookPanel.disposed.connect(this.dispose, this);
        this.init();
    }
    dispose() {
        _lumino_signaling__WEBPACK_IMPORTED_MODULE_1__.Signal.disconnectAll(this);
    }
    event(_, args) {
        var _a;
        if (args.header.msg_type == "error") {
            let cells = [
                {
                    id: (_a = this._notebookPanel.content.activeCell) === null || _a === void 0 ? void 0 : _a.model.id,
                    index: this._notebookPanel.content.activeCellIndex
                }
            ];
            this._cellErrored.emit({
                event_name: "cell_errored",
                cells: cells,
                notebookPanel: this._notebookPanel
            });
        }
    }
    enable() {
        (async () => {
            await this._notebookPanel.revealed;
            this._notebookPanel.sessionContext.iopubMessage.connect(this.event, this);
        })();
    }
    disable() {
        this._notebookPanel.sessionContext.iopubMessage.disconnect(this.event, this);
    }
    get cellErrored() {
        return this._cellErrored;
    }
}


/***/ }),

/***/ "./lib/handler.js":
/*!************************!*\
  !*** ./lib/handler.js ***!
  \************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "requestAPI": () => (/* binding */ requestAPI)
/* harmony export */ });
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/services */ "webpack/sharing/consume/default/@jupyterlab/services");
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__);


/**
 * Call the API extension
 *
 * @param endPoint API REST end point for the extension
 * @param init Initial values for the request
 * @returns The response body interpreted as JSON
 */
async function requestAPI(endPoint = '', init = {}) {
    // Make request to Jupyter API
    const settings = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.makeSettings();
    const requestUrl = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__.URLExt.join(settings.baseUrl, 'etc-jupyterlab-telemetry-library', // API Namespace
    endPoint);
    let response;
    try {
        response = await _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.makeRequest(requestUrl, init, settings);
    }
    catch (error) {
        throw new _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.NetworkError(error);
    }
    let data = await response.text();
    if (data.length > 0) {
        try {
            data = JSON.parse(data);
        }
        catch (error) {
            console.log('Not a JSON response body.', response);
        }
    }
    if (!response.ok) {
        throw new _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.ResponseError(response, data.message || data);
    }
    return data;
}


/***/ }),

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "IETCJupyterLabTelemetryLibraryFactory": () => (/* binding */ IETCJupyterLabTelemetryLibraryFactory),
/* harmony export */   "ETCJupyterLabTelemetryLibrary": () => (/* binding */ ETCJupyterLabTelemetryLibrary),
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _educational_technology_collective_etc_jupyterlab_notebook_state_provider__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @educational-technology-collective/etc_jupyterlab_notebook_state_provider */ "webpack/sharing/consume/default/@educational-technology-collective/etc_jupyterlab_notebook_state_provider");
/* harmony import */ var _educational_technology_collective_etc_jupyterlab_notebook_state_provider__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_educational_technology_collective_etc_jupyterlab_notebook_state_provider__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _events__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./events */ "./lib/events.js");
/* harmony import */ var _handler__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./handler */ "./lib/handler.js");





const PLUGIN_ID = '@educational-technology-collective/etc_jupyterlab_telemetry_library:plugin';
const IETCJupyterLabTelemetryLibraryFactory = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_1__.Token(PLUGIN_ID);
class ETCJupyterLabTelemetryLibraryFactory {
    constructor({ config }) {
        this._config = config;
    }
    create({ notebookPanel, config }) {
        return new ETCJupyterLabTelemetryLibrary({ notebookPanel, config: this._config });
    }
}
class ETCJupyterLabTelemetryLibrary {
    constructor({ notebookPanel, config }) {
        this.notebookOpenEvent = new _events__WEBPACK_IMPORTED_MODULE_3__.NotebookOpenEvent({
            notebookPanel: notebookPanel,
            config: config
        });
        this.notebookSaveEvent = new _events__WEBPACK_IMPORTED_MODULE_3__.NotebookSaveEvent({
            notebookPanel: notebookPanel,
            config: config
        });
        this.cellExecutionEvent = new _events__WEBPACK_IMPORTED_MODULE_3__.CellExecutionEvent({
            notebookPanel: notebookPanel,
            config: config
        });
        this.cellErrorEvent = new _events__WEBPACK_IMPORTED_MODULE_3__.CellErrorEvent({
            notebookPanel: notebookPanel,
            config: config
        });
        this.notebookScrollEvent = new _events__WEBPACK_IMPORTED_MODULE_3__.NotebookScrollEvent({
            notebookPanel: notebookPanel,
            config: config
        });
        this.activeCellChangeEvent = new _events__WEBPACK_IMPORTED_MODULE_3__.ActiveCellChangeEvent({
            notebookPanel: notebookPanel,
            config: config
        });
        this.cellAddEvent = new _events__WEBPACK_IMPORTED_MODULE_3__.CellAddEvent({
            notebookPanel: notebookPanel,
            config: config
        });
        this.cellRemoveEvent = new _events__WEBPACK_IMPORTED_MODULE_3__.CellRemoveEvent({
            notebookPanel: notebookPanel,
            config: config
        });
    }
}
/**
 * Initialization data for the @educational-technology-collective/etc_jupyterlab_telemetry_extension extension.
 */
const plugin = {
    id: PLUGIN_ID,
    autoStart: true,
    provides: IETCJupyterLabTelemetryLibraryFactory,
    requires: [_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__.INotebookTracker, _educational_technology_collective_etc_jupyterlab_notebook_state_provider__WEBPACK_IMPORTED_MODULE_2__.IETCJupyterLabNotebookStateProvider],
    activate: async (app, notebookTracker, etcJupyterLabNotebookStateProvider) => {
        console.log(`The JupyterLab plugin ${PLUGIN_ID} is activated!`);
        let config = await (0,_handler__WEBPACK_IMPORTED_MODULE_4__.requestAPI)("config");
        let etcJupyterLabTelemetryLibraryFactory = new ETCJupyterLabTelemetryLibraryFactory({ config });
        // // TEST
        // class MessageAdapter {
        //   constructor() { }
        //   log(sender: any, args: any) {
        //     let notebookPanel = args.notebookPanel;
        //     delete args.notebookPanel;
        //     let notebookState = etcJupyterLabNotebookStateProvider.getNotebookState({ notebookPanel: notebookPanel })
        //     let data = {
        //       ...args, ...notebookState
        //     }
        //     console.log("etc_jupyterlab_telemetry_extension", data);
        //   }
        // }
        // let messageAdapter = new MessageAdapter();
        // notebookTracker.widgetAdded.connect(async (sender: INotebookTracker, notebookPanel: NotebookPanel) => {
        //   etcJupyterLabNotebookStateProvider.addNotebookPanel({ notebookPanel });
        //   let etcJupyterLabTelemetryLibrary = etcJupyterLabTelemetryLibraryFactory.create({ notebookPanel, config });
        //   etcJupyterLabTelemetryLibrary.notebookOpenEvent.notebookOpened.connect(messageAdapter.log);
        //   etcJupyterLabTelemetryLibrary.notebookSaveEvent.notebookSaved.connect(messageAdapter.log);
        //   etcJupyterLabTelemetryLibrary.activeCellChangeEvent.activeCellChanged.connect(messageAdapter.log);
        //   etcJupyterLabTelemetryLibrary.cellAddEvent.cellAdded.connect(messageAdapter.log);
        //   etcJupyterLabTelemetryLibrary.cellRemoveEvent.cellRemoved.connect(messageAdapter.log);
        //   etcJupyterLabTelemetryLibrary.notebookScrollEvent.notebookScrolled.connect(messageAdapter.log);
        //   etcJupyterLabTelemetryLibrary.cellExecutionEvent.cellExecuted.connect(messageAdapter.log);
        //   etcJupyterLabTelemetryLibrary.cellErrorEvent.cellErrored.connect(messageAdapter.log);
        // });
        // // TEST
        return etcJupyterLabTelemetryLibraryFactory;
    }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugin);


/***/ })

}]);
//# sourceMappingURL=lib_index_js.6f5994679b93f4c13935.js.map