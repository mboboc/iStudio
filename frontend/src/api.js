import Cookies from "js-cookie";

class Api {
  _verb(url, body, method, headers = null) {
    return fetch(url, {
      method: method,
      headers: {
        ...headers,
        "X-CSRFToken": Cookies.get("csrftoken"),
      },
      body,
    });
  }

  _verbJson(url, data, method) {
    return this._verb(url, JSON.stringify(data), method, {
      "Content-Type": "application/json",
    });
  }

  _postJson(url, data) {
    return this._verbJson(url, data, "POST");
  }

  async _handleErrors(response) {
    const result = await response.json();
    if (result.ok !== true) {
      throw new Error(`Something happened: ${JSON.stringify(result)}`);
    }
    return result;
  }

  async saveForm(url, data) {
    const response = await this._postJson(url, data);
    if (response.status >= 400) {
      throw new Error(
        `Failed to save form: ${response.status} ${response.statusText}`
      );
    }
    // await this._handleErrors(response);
    return response
  }
}

export default new Api();