"use strict";
(self["webpackChunkjupyterlab_wipp_plugin_creator"] = self["webpackChunkjupyterlab_wipp_plugin_creator"] || []).push([["lib_index_js"],{

/***/ "./lib/addedFilesWidget.js":
/*!*********************************!*\
  !*** ./lib/addedFilesWidget.js ***!
  \*********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "AddedFilesWidget": () => (/* binding */ AddedFilesWidget)
/* harmony export */ });
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _extensionConstants__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./extensionConstants */ "./lib/extensionConstants.js");


class AddedFilesWidget extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__.Widget {
    constructor(state) {
        super();
        this._addedFileNames = [];
        this._state = state;
        this._addedFileDiv = document.createElement('p');
        this.node.appendChild(this._addedFileDiv);
        let button = document.createElement('button');
        button.innerHTML = 'Update list of files';
        button.onclick = () => this.update();
        this.node.appendChild(button);
        this.update();
    }
    onUpdateRequest(msg) {
        this._state.fetch(_extensionConstants__WEBPACK_IMPORTED_MODULE_1__.ExtensionConstants.dbkey).then(response => {
            this._addedFileNames = response;
            let text = 'Added Files: <br>';
            if (this._addedFileNames) {
                for (let i = 0; i < this._addedFileNames.length; i++) {
                    text += this._addedFileNames[i] + "<br>";
                }
            }
            this._addedFileDiv.innerHTML = text;
        });
    }
    getValue() {
        return this._addedFileNames;
    }
}


/***/ }),

/***/ "./lib/extensionConstants.js":
/*!***********************************!*\
  !*** ./lib/extensionConstants.js ***!
  \***********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "ExtensionConstants": () => (/* binding */ ExtensionConstants)
/* harmony export */ });
class ExtensionConstants {
}
ExtensionConstants.dbkey = 'wipp-plugin-creator:data';


/***/ }),

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/application */ "webpack/sharing/consume/default/@jupyterlab/application");
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/filebrowser */ "webpack/sharing/consume/default/@jupyterlab/filebrowser");
/* harmony import */ var _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/statedb */ "webpack/sharing/consume/default/@jupyterlab/statedb");
/* harmony import */ var _jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _extensionConstants__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./extensionConstants */ "./lib/extensionConstants.js");
/* harmony import */ var _sidebar__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./sidebar */ "./lib/sidebar.js");
/* harmony import */ var _style_logo_svg__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../style/logo.svg */ "./style/logo.svg");






// import { ISignal, Signal } from '@lumino/signaling';

const logoIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__.LabIcon({
    name: 'wipp-plugin-builder:logo',
    svgstr: _style_logo_svg__WEBPACK_IMPORTED_MODULE_4__["default"]
});
let filepaths = [];
// let _stateChanged = new Signal<ButtonWidget, ICount>(this);
const plugin = {
    id: 'jupyterlab_wipp_plugin_creator:plugin',
    autoStart: true,
    requires: [_jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_1__.IFileBrowserFactory, _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILabShell, _jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_2__.IStateDB],
    activate: (app, factory, labShell, state) => {
        // Initialzie dbkey if not in IStateDB
        state.list().then(response => {
            let keys = response.ids;
            if (keys.indexOf(_extensionConstants__WEBPACK_IMPORTED_MODULE_5__.ExtensionConstants.dbkey) === -1) {
                state.save(_extensionConstants__WEBPACK_IMPORTED_MODULE_5__.ExtensionConstants.dbkey, filepaths);
            }
        });
        // Create the WIPP sidebar panel
        const sidebar = new _sidebar__WEBPACK_IMPORTED_MODULE_6__.CreatorSidebar(state);
        sidebar.id = 'wipp-labextension:plugin';
        sidebar.title.icon = logoIcon;
        sidebar.title.caption = 'WIPP Plugin Creator';
        labShell.add(sidebar, 'left', { rank: 200 });
        // Add context menu command, right click file browser to register marked files to be converted to plugin
        var filepath = '';
        const addFileToPluginContextMenuCommandID = 'wipp-plugin-creator-add-context-menu';
        app.commands.addCommand(addFileToPluginContextMenuCommandID, {
            label: 'Add to the new WIPP plugin',
            iconClass: 'jp-MaterialIcon jp-AddIcon',
            isVisible: () => ['notebook', 'file'].includes(factory.tracker.currentWidget.selectedItems().next().type),
            execute: () => {
                filepath = factory.tracker.currentWidget.selectedItems().next().path;
                state.fetch(_extensionConstants__WEBPACK_IMPORTED_MODULE_5__.ExtensionConstants.dbkey).then(response => {
                    filepaths = response;
                    if (filepaths.indexOf(filepath) === -1) {
                        filepaths.push(filepath);
                    }
                    else {
                        console.log(`${filepath} was already added`);
                    }
                    state.save(_extensionConstants__WEBPACK_IMPORTED_MODULE_5__.ExtensionConstants.dbkey, filepaths);
                });
            }
        });
        // Add command to context menu
        const selectorItem = '.jp-DirListing-item[data-isdir]';
        app.contextMenu.addItem({
            command: addFileToPluginContextMenuCommandID,
            selector: selectorItem
        });
    }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugin);


/***/ }),

/***/ "./lib/sidebar.js":
/*!************************!*\
  !*** ./lib/sidebar.js ***!
  \************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "CreatorSidebar": () => (/* binding */ CreatorSidebar)
/* harmony export */ });
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _addedFilesWidget__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./addedFilesWidget */ "./lib/addedFilesWidget.js");
/* harmony import */ var _WippPluginSchema_json__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./WippPluginSchema.json */ "./lib/WippPluginSchema.json");
/* harmony import */ var _rjsf_core__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @rjsf/core */ "./node_modules/@rjsf/core/dist/es/index.js");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_3__);



// import { requestAPI } from './handler';



class CreatorSidebar extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__.Widget {
    /**
    * Create a new WIPP plugin creator sidebar.
    */
    constructor(state) {
        super();
        this.addClass('wipp-pluginCreatorSidebar');
        // Define Widget layout
        let layout = (this.layout = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__.PanelLayout());
        let title = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__.Widget();
        let h1 = document.createElement('h1');
        h1.innerText = "Create New Plugin";
        title.node.appendChild(h1);
        layout.addWidget(title);
        //necessary or plugin will not activate
        const schema = _WippPluginSchema_json__WEBPACK_IMPORTED_MODULE_4__;
        this._addFileWidget = new _addedFilesWidget__WEBPACK_IMPORTED_MODULE_5__.AddedFilesWidget(state);
        layout.addWidget(this._addFileWidget);
        // const formData: any = {
        // version: "0.1.0",
        // requirements: [''],
        // inputs: [{}],
        // outputs: [{}],
        // };
        // const extraErrors: any = {
        // name: {
        // __errors: ["some error that got added as a prop"],
        // }
        // };
        this._form = _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ReactWidget.create(react__WEBPACK_IMPORTED_MODULE_3___default().createElement(_rjsf_core__WEBPACK_IMPORTED_MODULE_2__["default"], { schema: schema }));
        // this._form = new SchemaForm(schema, { formData: formData });
        layout.addWidget(this._form);
        const runButtonWidget = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__.Widget();
        const runButton = document.createElement('button');
        runButton.className = 'run';
        runButton.onclick = () => {
            this.submit();
        };
        runButton.innerText = "Create Plugin";
        runButtonWidget.node.appendChild(runButton);
        layout.addWidget(runButtonWidget);
    }
    //Sidebar constructor ends
    submit() {
        console.log('Button clicked');
        //Create API request on submit
        // let formValue = this._form.getValue()
        // // console.log(formValue);
        // let request = {
        // formdata: formValue.formData,
        // addedfilepaths: this._addFileWidget.getValue()
        // };
        // if (formValue.errors !== null) {
        // var fullRequest = {
        // method: 'POST',
        // body: JSON.stringify(request)
        // };
        // requestAPI<any>('createplugin', fullRequest)
        // .then(response => {
        // console.log('POST request sent.')
        // })
        // .catch(() => console.log('There is an error making POST CreatePlugin API request.'));
        // }
        // else {
        // console.log(`Schema form data returns with an error`);
        // console.log(formValue.errors)
        // }
    }
}


/***/ }),

/***/ "./style/logo.svg":
/*!************************!*\
  !*** ./style/logo.svg ***!
  \************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ("<svg width=\"1792\" height=\"1792\" viewBox=\"0 0 1792 1792\" xmlns=\"http://www.w3.org/2000/svg\">\n    <path class=\"jp-icon3 jp-icon-selectable\" fill=\"#616161\" d=\"M896 1629l640-349v-636l-640 233v752zm-64-865l698-254-698-254-698 254zm832-252v768q0 35-18 65t-49 47l-704 384q-28 16-61 16t-61-16l-704-384q-31-17-49-47t-18-65v-768q0-40 23-73t61-47l704-256q22-8 44-8t44 8l704 256q38 14 61 47t23 73z\"/>\n</svg> ");

/***/ }),

/***/ "./lib/WippPluginSchema.json":
/*!***********************************!*\
  !*** ./lib/WippPluginSchema.json ***!
  \***********************************/
/***/ ((module) => {

module.exports = JSON.parse('{"$schema":"http://json-schema.org/draft-07/schema#","$id":"https://raw.githubusercontent.com/usnistgov/WIPP-Plugins-base-templates/master/plugin-manifest/schema/wipp-plugin-manifest-schema.json","type":"object","title":"WIPP Plugin manifest","default":null,"required":["name","version","title","description","inputs","outputs","ui"],"properties":{"name":{"$id":"#/properties/name","type":"string","title":"Name of the plugin","default":"","examples":["My Awesome Plugin"],"minLength":1,"pattern":"^(.*)$"},"file":{"$id":"#/properties/file","type":"array","items":{"type":"string","format":"data-url"},"title":"Select files"},"requirements":{"type":"array","items":{"type":"string"},"title":"Requirements"},"version":{"$id":"#/properties/version","type":"string","title":"Plugin version","default":"","examples":["1.0.0"],"minLength":1,"pattern":"^(.*)$"},"title":{"$id":"#/properties/title","type":"string","title":"Plugin title","default":"","examples":["My really awesome plugin"],"minLength":1,"pattern":"^(.*)$"},"description":{"$id":"#/properties/description","type":"string","title":"Description","default":"","examples":["My awesome segmentation algorithm"],"minLength":1,"pattern":"^(.*)$"},"author":{"$id":"#/properties/author","type":["string","null"],"title":"Author(s)","default":"","examples":["FirstName LastName"],"pattern":"^(.*)$"},"institution":{"$id":"#/properties/institution","type":["string","null"],"title":"Institution","default":"","examples":["National Institute of Standards and Technology"],"pattern":"^(.*)$"},"repository":{"$id":"#/properties/repository","type":["string","null"],"title":"Source code repository","default":"","examples":["https://github.com/usnistgov/WIPP"],"format":"uri"},"website":{"$id":"#/properties/website","type":["string","null"],"title":"Website","default":"","examples":["http://usnistgov.github.io/WIPP"],"format":"uri"},"citation":{"$id":"#/properties/citation","type":["string","null"],"title":"Citation","default":"","examples":["Peter Bajcsy, Joe Chalfoun, and Mylene Simon (2018). Web Microanalysis of Big Image Data. Springer-Verlag International"],"pattern":"^(.*)$"},"inputs":{"$id":"#/properties/inputs","type":"array","title":"List of Inputs","description":"Defines inputs to the plugin","default":null,"uniqueItems":true,"items":{"$id":"#/properties/inputs/items","type":"object","title":"Input","description":"Plugin input","default":null,"required":["name","type","description"],"properties":{"name":{"$id":"#/properties/inputs/items/properties/name","type":"string","title":"Input name","description":"Input name as expected by the plugin CLI","default":"","examples":["inputImages","fileNamePattern","thresholdValue"],"pattern":"^[a-zA-Z0-9][-a-zA-Z0-9]*$"},"type":{"$id":"#/properties/inputs/items/properties/type","type":"string","enum":["collection","stitchingVector","tensorflowModel","csvCollection","pyramid","notebook","string","number","integer","enum","array","boolean"],"title":"Input Type","examples":["collection","string","number"]},"description":{"$id":"#/properties/inputs/items/properties/description","type":"string","title":"Input description","examples":["Input Images"],"pattern":"^(.*)$"},"required":{"$id":"#/properties/inputs/items/properties/required","type":"boolean","title":"Required input","description":"Whether an input is required or not","default":true,"examples":[true]}},"allOf":[{"if":{"properties":{"type":{"const":"enum"}}},"then":{"properties":{"options":{"$id":"#/properties/inputs/items/properties/options","type":"object","title":"Input options","properties":{"values":{"type":"array","description":"List of possible values","items":{"type":"string"},"uniqueItems":true}}}}}},{"if":{"properties":{"type":{"const":"array"}}},"then":{"properties":{"options":{"$id":"#/properties/inputs/items/properties/options","type":"object","title":"Input options","properties":{"items":{"$id":"#/properties/inputs/items/properties/options/properties/items","type":"object","title":"List of array items","description":"Possible values for the input array","default":{},"required":["type","title","oneOf","default","widget","minItems","uniqueItems"],"properties":{"type":{"$id":"#/properties/inputs/items/properties/options/properties/items/properties/type","type":"string","title":"Items type","description":"Type of the items to be selected","enum":["string"],"examples":["string"]},"title":{"$id":"#/properties/inputs/items/properties/options/properties/items/properties/title","type":"string","title":"Selection title","description":"Title of the item selection section in the form","default":"","examples":["Select feature"]},"oneOf":{"$id":"#/properties/inputs/items/properties/options/properties/items/properties/oneOf","type":"array","title":"Possible items","description":"List of possible items","default":[],"items":{"$id":"#/properties/inputs/items/properties/options/properties/items/properties/oneOf/items","type":"object","title":"Items definition","description":"Description of the possible items","default":{},"required":["description","enum"],"properties":{"description":{"$id":"#/properties/inputs/items/properties/options/properties/items/properties/oneOf/items/properties/description","type":"string","title":"Description","description":"Description of the value that will appear in the form","default":"","examples":["Area"]},"enum":{"$id":"#/properties/inputs/items/properties/options/properties/items/properties/oneOf/items/properties/enum","type":"array","title":"Value","description":"Values of the selected item","default":[],"items":{"$id":"#/properties/inputs/items/properties/options/properties/items/properties/oneOf/items/properties/enum/items","type":"string","title":"List of values","description":"List of values associated with the selected item (usually one value)","default":"","examples":["Feature2DJava_Area"]}}},"examples":[{"description":"Area","enum":["Feature2DJava_Area"]},{"enum":["Feature2DJava_Mean"],"description":"Mean"}]}},"default":{"$id":"#/properties/inputs/items/properties/options/properties/items/properties/default","type":"string","title":"Default value","description":"Value selected by default (must be one of the possible values)","default":"","examples":["Feature2DJava_Area"]},"widget":{"$id":"#/properties/inputs/items/properties/options/properties/items/properties/widget","type":"string","title":"Item selection widget","description":"How items can be selected (select -> dropdown list with add/remove buttons, checkbox -> multi-selection from list)","enum":["select","checkbox"],"examples":["select"]},"minItems":{"$id":"#/properties/inputs/items/properties/options/properties/items/properties/minItems","type":"integer","title":"Minumum number of items","description":"Minumum number of items","default":0,"examples":[1]},"uniqueItems":{"$id":"#/properties/inputs/items/properties/options/properties/items/properties/uniqueItems","type":["string","boolean"],"title":"Uniqueness of the items","description":"Whether items in the array have to be unique","examples":["true",true]}},"examples":[{"type":"string","widget":"select","uniqueItems":"true","default":"Feature2DJava_Area","minItems":1,"title":"Select feature","oneOf":[{"description":"Area","enum":["Feature2DJava_Area"]},{"description":"Mean","enum":["Feature2DJava_Mean"]}]}]}}}}}}]}},"outputs":{"$id":"#/properties/outputs","type":"array","title":"List of Outputs","description":"Defines the outputs of the plugin","default":null,"items":{"$id":"#/properties/outputs/items","type":"object","title":"Plugin output","default":null,"required":["name","type","description"],"properties":{"name":{"$id":"#/properties/outputs/items/properties/name","type":"string","title":"Output name","default":"","examples":["outputCollection"],"pattern":"^[a-zA-Z0-9][-a-zA-Z0-9]*$"},"type":{"$id":"#/properties/outputs/items/properties/type","type":"string","enum":["collection","stitchingVector","tensorflowModel","tensorboardLogs","csvCollection","pyramid"],"title":"Output type","examples":["stitchingVector","collection"]},"description":{"$id":"#/properties/outputs/items/properties/description","type":"string","title":"Output description","examples":["Output collection"],"pattern":"^(.*)$"}}}}}}');

/***/ })

}]);
//# sourceMappingURL=lib_index_js.0f3f50b3cbd0f9f2529a.js.map