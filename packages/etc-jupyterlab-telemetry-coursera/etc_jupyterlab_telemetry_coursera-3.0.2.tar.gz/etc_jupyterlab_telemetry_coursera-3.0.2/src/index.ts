import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

import { INotebookTracker, NotebookPanel } from '@jupyterlab/notebook';

import {
  IETCJupyterLabTelemetryLibraryFactory
} from "@educational-technology-collective/etc_jupyterlab_telemetry_library";

import { IETCJupyterLabNotebookStateProvider } from "@educational-technology-collective/etc_jupyterlab_notebook_state_provider";

import { IValidateButtonExtension } from "@educational-technology-collective/etc_jupyterlab_nbgrader_validate";

import { requestAPI } from './handler';

import { ETCJupyterLabTelemetryValidateButton } from "./etc_jupyterlab_telemetry_validate_button";

const PLUGIN_ID = '@educational-technology-collective/etc_jupyterlab_telemetry_coursera:plugin';

export class AWSAPIGatewayAdapter {

  private _userId: Promise<string>;
  private _etcJupyterLabNotebookStateProvider: IETCJupyterLabNotebookStateProvider;

  constructor(
    { etcJupyterLabNotebookStateProvider }:
      { etcJupyterLabNotebookStateProvider: IETCJupyterLabNotebookStateProvider }
  ) {

    this._etcJupyterLabNotebookStateProvider = etcJupyterLabNotebookStateProvider;

    this._userId = (async () => {

      try { // to get the user id.
        return await requestAPI<string>("id");
      } catch (e) {
        console.error(`Error on GET id.\n${e}`);
        return "UNDEFINED";
      }
      //  This request is specific to the Coursera environment; hence, it may not be relevant in other contexts.
      //  The request for the `id` resource will return the value of the WORKSPACE_ID environment variable that is assigned on the server.
    })();
  }

  adaptMessage(sender: any, data: any): void {

    (async () => {
      try {

        let notebookState = this._etcJupyterLabNotebookStateProvider.getNotebookState({
          notebookPanel: data.notebookPanel
        });

        let notebookPath = data.notebookPanel.context.path;

        delete data.notebookPanel;

        data = {
          ...data,
          ...notebookState,
          ...{
            user_id: await this._userId,
            notebook_path: notebookPath
          }
        }

        console.log(data);

        let response = await requestAPI<string>("s3", { method: "POST", body: JSON.stringify(data) });

        //console.log(response);
      }
      catch (e) {
        console.error(e);
      }
    })();
  }
}

/**
 * Initialization data for the @educational-technology-collective/etc_jupyterlab_telemetry_coursera extension.
 */
const plugin: JupyterFrontEndPlugin<void> = {
  id: PLUGIN_ID,
  autoStart: true,
  requires: [
    INotebookTracker,
    IETCJupyterLabNotebookStateProvider,
    IETCJupyterLabTelemetryLibraryFactory,
    IValidateButtonExtension
  ],
  activate: (
    app: JupyterFrontEnd,
    notebookTracker: INotebookTracker,
    etcJupyterLabNotebookStateProvider: IETCJupyterLabNotebookStateProvider,
    etcJupyterLabTelemetryLibraryFactory: IETCJupyterLabTelemetryLibraryFactory,
    validateButtonExtension: IValidateButtonExtension,
  ) => {
    console.log(`The JupyterLab plugin ${PLUGIN_ID} is activated!`);

    let messageAdapter = new AWSAPIGatewayAdapter({ etcJupyterLabNotebookStateProvider });

    notebookTracker.widgetAdded.connect(async (sender: INotebookTracker, notebookPanel: NotebookPanel) => {

      etcJupyterLabNotebookStateProvider.addNotebookPanel({ notebookPanel });

      let etcJupyterLabTelemetryLibrary = etcJupyterLabTelemetryLibraryFactory.create({
        notebookPanel
      });

      etcJupyterLabTelemetryLibrary.notebookOpenEvent.notebookOpened.connect(messageAdapter.adaptMessage, messageAdapter);
      etcJupyterLabTelemetryLibrary.notebookSaveEvent.notebookSaved.connect(messageAdapter.adaptMessage, messageAdapter);
      etcJupyterLabTelemetryLibrary.activeCellChangeEvent.activeCellChanged.connect(messageAdapter.adaptMessage, messageAdapter);
      etcJupyterLabTelemetryLibrary.cellAddEvent.cellAdded.connect(messageAdapter.adaptMessage, messageAdapter);
      etcJupyterLabTelemetryLibrary.cellRemoveEvent.cellRemoved.connect(messageAdapter.adaptMessage, messageAdapter);
      etcJupyterLabTelemetryLibrary.notebookScrollEvent.notebookScrolled.connect(messageAdapter.adaptMessage, messageAdapter);
      etcJupyterLabTelemetryLibrary.cellExecutionEvent.cellExecuted.connect(messageAdapter.adaptMessage, messageAdapter);
      etcJupyterLabTelemetryLibrary.cellErrorEvent.cellErrored.connect(messageAdapter.adaptMessage, messageAdapter);

      let etcJupyterLabTelemetryValidateButton = new ETCJupyterLabTelemetryValidateButton({
        notebookPanel,
        validateButtonExtension
      });

      etcJupyterLabTelemetryValidateButton.validateButtonClicked.connect(messageAdapter.adaptMessage, messageAdapter);
      etcJupyterLabTelemetryValidateButton.validationResultsDisplayed.connect(messageAdapter.adaptMessage, messageAdapter);
      etcJupyterLabTelemetryValidateButton.validationResultsDismissed.connect(messageAdapter.adaptMessage, messageAdapter);

    });
  }
};

export default plugin;
