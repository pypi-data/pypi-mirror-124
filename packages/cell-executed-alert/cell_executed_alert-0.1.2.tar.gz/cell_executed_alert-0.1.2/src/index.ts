import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

import {INotebookTracker} from "@jupyterlab/notebook";

import {ButtonExtension}  from "./button";

/**
 * Initialization data for the cell-executed-alert extension.
 */
const plugin: JupyterFrontEndPlugin<void> = {
  id: 'cell-executed-alert:plugin',
  autoStart: true,
  activate: (app: JupyterFrontEnd, tracker: INotebookTracker) => {
    let buttonExtension = new ButtonExtension();
    app.docRegistry.addWidgetExtension('Notebook', buttonExtension);
  }
};

export default plugin;
