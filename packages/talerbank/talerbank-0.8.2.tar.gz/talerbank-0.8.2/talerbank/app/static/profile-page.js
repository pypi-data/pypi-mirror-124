/*
  @licstart  The following is the entire license notice for the
  JavaScript code in this page.
  
  Copyright (C) 2014, 2015, 2016 Inria and GNUnet e.V.
  
  The JavaScript code in this page is free software: you can
  redistribute it and/or modify it under the terms of the GNU
  General Public License (GNU GPL) as published by the Free Software
  Foundation, either version 3 of the License, or (at your option)
  any later version.  The code is distributed WITHOUT ANY WARRANTY;
  without even the implied warranty of MERCHANTABILITY or FITNESS
  FOR A PARTICULAR PURPOSE.  See the GNU GPL for more details.
  
  As additional permission under GNU GPL version 3 section 7, you
  may distribute non-source (e.g., minimized or compacted) forms of
  that code without the copy of the GNU GPL normally required by
  section 4, provided you include this license notice and a URL
  through which recipients can access the Corresponding Source.
  
  @licend  The above is the entire license notice
  for the JavaScript code in this page. */

"use strict";


var bank_currency;
var precision;
var callback_url;
var reserve_pub;
var suggested_exchange;


/**
 * Get a constant stored in the DOM
 * as a meta tag.
 */
function getConst(name) {
  var metas = document.getElementsByTagName("meta");
  if (!(name in metas)) {
    return;
  }
  return metas[name].getAttribute("value");
}


/**
 * Parse fractional format (e.g. 42.12 EUR) into
 * Taler amount.
 */
function parseAmount(amount_str) {
  var re = /([0-9]+)(\.?[0-9][0-9]?)? ([A-Z]+)/;
  var amount = re.exec(amount_str);
  if (amount == null || amount[0] != amount_str){
    window.alert("Incorrect amount entered, give in the"
	             + " form 'XY.Z EUR' or 'XY EUR'");
    return null;
  }
  var amount_fraction = 0;
    if (amount[2] != null) // fractional part given
      amount_fraction = Number("0." + amount[2]) * 1000000;
  if (amount[1] + amount_fraction == 0)
    return null;
  return {
    value: Number(amount[1]),
    fraction: amount_fraction,
    currency: amount[amount.length - 1]
  };
};


function init() {
  bank_currency = getConst("currency");
  precision = getConst("precision");
  callback_url = getConst("callback-url");
  reserve_pub = getConst("reserve-pub");
  suggested_exchange = getConst("suggested-exchange");
  if (reserve_pub) {
    console.log("confirming reserve", reserve_pub);
    taler.confirmReserve(reserve_pub); 
  }
  document.getElementById("select-exchange").onclick = function () {
    var form = document.getElementById("reserve-form");
    var amount = {
      value: parseInt(form.elements["reserve-amount"].value),
      fraction: 0,
      currency: bank_currency
    };
    console.log("callback_url", callback_url);
    taler.createReserve(callback_url, amount, ["test"], suggested_exchange);
  };
}


if (document.readyState == "loading") {
  document.addEventListener("DOMContentLoaded", init);
} else {
  init();
}
