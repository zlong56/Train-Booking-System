import { Config } from '../config';
import MemoryStorage from './memory';
import Storage from './storage';
import ServerStorage from './server';
import log from '../util/log';
import { decode, html } from '../util/html';

class StorageUtils {
  /**
   * Accepts a Config object and tries to guess and return a Storage type
   *
   * @param config
   */
  public static createFromConfig(config: Config): Storage<any> {
    let storage = null;
    // `data` array is provided
    if (config.data) {
      storage = new MemoryStorage(config.data);
    }

    if (config.from) {
      storage = new MemoryStorage(this.tableElementToArray(config.from));
      // remove the source table element from the DOM
      config.from.style.display = 'none';
    }

    if (config.server) {
      storage = new ServerStorage(config.server);
    }

    if (!storage) {
      log.error('Could not determine the storage type', true);
    }

    return storage;
  }

  /**
   * Accepts a HTML table element and converts it into a 2D array of data
   *
   * TODO: This function can be a step in the pipeline: Convert Table -> Load into a memory storage -> ...
   *
   * @param element
   */
  static tableElementToArray(element: HTMLElement): any[][] {
    const arr = [];
    const tbody = element.querySelector('tbody');
    const rows = tbody.querySelectorAll('tr');

    for (const row of rows as any) {
      const cells: HTMLElement[] = row.querySelectorAll('td');
      const parsedRow = [];

      for (const cell of cells) {
        // try to capture a TD with single text element first
        if (
          cell.childNodes.length === 1 &&
          cell.childNodes[0].nodeType === Node.TEXT_NODE
        ) {
          parsedRow.push(decode(cell.innerHTML));
        } else {
          parsedRow.push(html(cell.innerHTML));
        }
      }

      arr.push(parsedRow);
    }

    return arr;
  }
}

export default StorageUtils;
