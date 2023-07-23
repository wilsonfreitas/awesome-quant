(function() {

// some helper functions: using a global object DTWidget so that it can be used
// in JS() code, e.g. datatable(options = list(foo = JS('code'))); unlike R's
// dynamic scoping, when 'code' is eval()'ed, JavaScript does not know objects
// from the "parent frame", e.g. JS('DTWidget') will not work unless it was made
// a global object
var DTWidget = {};

// 123456666.7890 -> 123,456,666.7890
var markInterval = function(d, digits, interval, mark, decMark, precision) {
  x = precision ? d.toPrecision(digits) : d.toFixed(digits);
  if (!/^-?[\d.]+$/.test(x)) return x;
  var xv = x.split('.');
  if (xv.length > 2) return x;  // should have at most one decimal point
  xv[0] = xv[0].replace(new RegExp('\\B(?=(\\d{' + interval + '})+(?!\\d))', 'g'), mark);
  return xv.join(decMark);
};

DTWidget.formatCurrency = function(data, currency, digits, interval, mark, decMark, before, zeroPrint) {
  var d = parseFloat(data);
  if (isNaN(d)) return '';
  if (zeroPrint !== null && d === 0.0) return zeroPrint;
  var res = markInterval(d, digits, interval, mark, decMark);
  res = before ? (/^-/.test(res) ? '-' + currency + res.replace(/^-/, '') : currency + res) :
    res + currency;
  return res;
};

DTWidget.formatString = function(data, prefix, suffix) {
  var d = data;
  if (d === null) return '';
  return prefix + d + suffix;
};

DTWidget.formatPercentage = function(data, digits, interval, mark, decMark, zeroPrint) {
  var d = parseFloat(data);
  if (isNaN(d)) return '';
  if (zeroPrint !== null && d === 0.0) return zeroPrint;
  return markInterval(d * 100, digits, interval, mark, decMark) + '%';
};

DTWidget.formatRound = function(data, digits, interval, mark, decMark, zeroPrint) {
  var d = parseFloat(data);
  if (isNaN(d)) return '';
  if (zeroPrint !== null && d === 0.0) return zeroPrint;
  return markInterval(d, digits, interval, mark, decMark);
};

DTWidget.formatSignif = function(data, digits, interval, mark, decMark, zeroPrint) {
  var d = parseFloat(data);
  if (isNaN(d)) return '';
  if (zeroPrint !== null && d === 0.0) return zeroPrint;
  return markInterval(d, digits, interval, mark, decMark, true);
};

DTWidget.formatDate = function(data, method, params) {
  var d = data;
  if (d === null) return '';
  // (new Date('2015-10-28')).toDateString() may return 2015-10-27 because the
  // actual time created could be like 'Tue Oct 27 2015 19:00:00 GMT-0500 (CDT)',
  // i.e. the date-only string is treated as UTC time instead of local time
  if ((method === 'toDateString' || method === 'toLocaleDateString') && /^\d{4,}\D\d{2}\D\d{2}$/.test(d)) {
    d = d.split(/\D/);
    d = new Date(d[0], d[1] - 1, d[2]);
  } else {
    d = new Date(d);
  }
  return d[method].apply(d, params);
};

window.DTWidget = DTWidget;

// A helper function to update the properties of existing filters
var setFilterProps = function(td, props) {
  // Update enabled/disabled state
  var $input = $(td).find('input').first();
  var searchable = $input.data('searchable');
  $input.prop('disabled', !searchable || props.disabled);

  // Based on the filter type, set its new values
  var type = td.getAttribute('data-type');
  if (['factor', 'logical'].includes(type)) {
    // Reformat the new dropdown options for use with selectize
    var new_vals = props.params.options.map(function(item) {
      return { text: item, value: item };
    });

    // Find the selectize object
    var dropdown = $(td).find('.selectized').eq(0)[0].selectize;

    // Note the current values
    var old_vals = dropdown.getValue();

    // Remove the existing values
    dropdown.clearOptions();

    // Add the new options
    dropdown.addOption(new_vals);

    // Preserve the existing values
    dropdown.setValue(old_vals);

  } else if (['number', 'integer', 'date', 'time'].includes(type)) {
    // Apply internal scaling to new limits. Updating scale not yet implemented.
    var slider = $(td).find('.noUi-target').eq(0);
    var scale = Math.pow(10, Math.max(0, +slider.data('scale') || 0));
    var new_vals = [props.params.min * scale, props.params.max * scale];

    // Note what the new limits will be just for this filter
    var new_lims = new_vals.slice();

    // Determine the current values and limits
    var old_vals = slider.val().map(Number);
    var old_lims = slider.noUiSlider('options').range;
    old_lims = [old_lims.min, old_lims.max];

    // Preserve the current values if filters have been applied; otherwise, apply no filtering
    if (old_vals[0] != old_lims[0]) {
      new_vals[0] = Math.max(old_vals[0], new_vals[0]);
    }

    if (old_vals[1] != old_lims[1]) {
      new_vals[1] = Math.min(old_vals[1], new_vals[1]);
    }

    // Update the endpoints of the slider
    slider.noUiSlider({
      start: new_vals,
      range: {'min': new_lims[0], 'max': new_lims[1]}
    }, true);
  }
};

var transposeArray2D = function(a) {
  return a.length === 0 ? a : HTMLWidgets.transposeArray2D(a);
};

var crosstalkPluginsInstalled = false;

function maybeInstallCrosstalkPlugins() {
  if (crosstalkPluginsInstalled)
    return;
  crosstalkPluginsInstalled = true;

  $.fn.dataTable.ext.afnFiltering.push(
    function(oSettings, aData, iDataIndex) {
      var ctfilter = oSettings.nTable.ctfilter;
      if (ctfilter && !ctfilter[iDataIndex])
        return false;

      var ctselect = oSettings.nTable.ctselect;
      if (ctselect && !ctselect[iDataIndex])
        return false;

      return true;
    }
  );
}

HTMLWidgets.widget({
  name: "datatables",
  type: "output",
  renderOnNullValue: true,
  initialize: function(el, width, height) {
    // in order that the type=number inputs return a number
    $.valHooks.number = {
      get: function(el) {
        var value = parseFloat(el.value);
        return isNaN(value) ? "" : value;
      }
    };
    $(el).html('&nbsp;');
    return {
      data: null,
      ctfilterHandle: new crosstalk.FilterHandle(),
      ctfilterSubscription: null,
      ctselectHandle: new crosstalk.SelectionHandle(),
      ctselectSubscription: null
    };
  },
  renderValue: function(el, data, instance) {
    if (el.offsetWidth === 0 || el.offsetHeight === 0) {
      instance.data = data;
      return;
    }
    instance.data = null;
    var $el = $(el);
    $el.empty();

    if (data === null) {
      $el.append('&nbsp;');
      // clear previous Shiny inputs (if any)
      for (var i in instance.clearInputs) instance.clearInputs[i]();
      instance.clearInputs = {};
      return;
    }

    var crosstalkOptions = data.crosstalkOptions;
    if (!crosstalkOptions) crosstalkOptions = {
      'key': null, 'group': null
    };
    if (crosstalkOptions.group) {
      maybeInstallCrosstalkPlugins();
      instance.ctfilterHandle.setGroup(crosstalkOptions.group);
      instance.ctselectHandle.setGroup(crosstalkOptions.group);
    }

    // if we are in the viewer then we always want to fillContainer and
    // and autoHideNavigation (unless the user has explicitly set these)
    if (window.HTMLWidgets.viewerMode) {
      if (!data.hasOwnProperty("fillContainer"))
        data.fillContainer = true;
      if (!data.hasOwnProperty("autoHideNavigation"))
        data.autoHideNavigation = true;
    }

    // propagate fillContainer to instance (so we have it in resize)
    instance.fillContainer = data.fillContainer;

    var cells = data.data;

    if (cells instanceof Array) cells = transposeArray2D(cells);

    $el.append(data.container);
    var $table = $el.find('table');
    if (data.class) $table.addClass(data.class);
    if (data.caption) $table.prepend(data.caption);

    if (!data.selection) data.selection = {
      mode: 'none', selected: null, target: 'row', selectable: null
    };
    if (HTMLWidgets.shinyMode && data.selection.mode !== 'none' &&
        data.selection.target === 'row+column') {
      if ($table.children('tfoot').length === 0) {
        $table.append($('<tfoot>'));
        $table.find('thead tr').clone().appendTo($table.find('tfoot'));
      }
    }

    // column filters
    var filterRow;
    switch (data.filter) {
      case 'top':
        $table.children('thead').append(data.filterHTML);
        filterRow = $table.find('thead tr:last td');
        break;
      case 'bottom':
        if ($table.children('tfoot').length === 0) {
          $table.append($('<tfoot>'));
        }
        $table.children('tfoot').prepend(data.filterHTML);
        filterRow = $table.find('tfoot tr:first td');
        break;
    }

    var options = { searchDelay: 1000 };
    if (cells !== null) $.extend(options, {
      data: cells
    });

    // options for fillContainer
    var bootstrapActive = typeof($.fn.popover) != 'undefined';
    if (instance.fillContainer) {

      // force scrollX/scrollY and turn off autoWidth
      options.scrollX = true;
      options.scrollY = "100px"; // can be any value, we'll adjust below

      // if we aren't paginating then move around the info/filter controls
      // to save space at the bottom and rephrase the info callback
      if (data.options.paging === false) {

        // we know how to do this cleanly for bootstrap, not so much
        // for other themes/layouts
        if (bootstrapActive) {
          options.dom = "<'row'<'col-sm-4'i><'col-sm-8'f>>" +
                        "<'row'<'col-sm-12'tr>>";
        }

        options.fnInfoCallback = function(oSettings, iStart, iEnd,
                                           iMax, iTotal, sPre) {
          return Number(iTotal).toLocaleString() + " records";
        };
      }
    }

    // auto hide navigation if requested
    // Note, this only works on client-side processing mode as on server-side,
    // cells (data.data) is null; In addition, we require the pageLength option
    // being provided explicitly to enable this. Despite we may be able to deduce
    // the default value of pageLength, it may complicate things so we'd rather
    // put this responsiblity to users and warn them on the R side.
    if (data.autoHideNavigation === true && data.options.paging !== false) {
      // strip all nav if length >= cells
      if ((cells instanceof Array) && data.options.pageLength >= cells.length)
        options.dom = bootstrapActive ? "<'row'<'col-sm-12'tr>>" : "t";
      // alternatively lean things out for flexdashboard mobile portrait
      else if (bootstrapActive && window.FlexDashboard && window.FlexDashboard.isMobilePhone())
        options.dom = "<'row'<'col-sm-12'f>>" +
                      "<'row'<'col-sm-12'tr>>"  +
                      "<'row'<'col-sm-12'p>>";
    }

    $.extend(true, options, data.options || {});

    var searchCols = options.searchCols;
    if (searchCols) {
      searchCols = searchCols.map(function(x) {
        return x === null ? '' : x.search;
      });
      // FIXME: this means I don't respect the escapeRegex setting
      delete options.searchCols;
    }

    // server-side processing?
    var server = options.serverSide === true;

    // use the dataSrc function to pre-process JSON data returned from R
    var DT_rows_all = [], DT_rows_current = [];
    if (server && HTMLWidgets.shinyMode && typeof options.ajax === 'object' &&
        /^session\/[\da-z]+\/dataobj/.test(options.ajax.url) && !options.ajax.dataSrc) {
      options.ajax.dataSrc = function(json) {
        DT_rows_all = $.makeArray(json.DT_rows_all);
        DT_rows_current = $.makeArray(json.DT_rows_current);
        var data = json.data;
        if (!colReorderEnabled()) return data;
        var table = $table.DataTable(), order = table.colReorder.order(), flag = true, i, j, row;
        for (i = 0; i < order.length; ++i) if (order[i] !== i) flag = false;
        if (flag) return data;
        for (i = 0; i < data.length; ++i) {
          row = data[i].slice();
          for (j = 0; j < order.length; ++j) data[i][j] = row[order[j]];
        }
        return data;
      };
    }

    var thiz = this;
    if (instance.fillContainer) $table.on('init.dt', function(e) {
      thiz.fillAvailableHeight(el, $(el).innerHeight());
    });
    // If the page contains serveral datatables and one of which enables colReorder,
    // the table.colReorder.order() function will exist but throws error when called.
    // So it seems like the only way to know if colReorder is enabled or not is to
    // check the options.
    var colReorderEnabled = function() { return "colReorder" in options; };
    var table = $table.DataTable(options);
    $el.data('datatable', table);

    // Unregister previous Crosstalk event subscriptions, if they exist
    if (instance.ctfilterSubscription) {
      instance.ctfilterHandle.off("change", instance.ctfilterSubscription);
      instance.ctfilterSubscription = null;
    }
    if (instance.ctselectSubscription) {
      instance.ctselectHandle.off("change", instance.ctselectSubscription);
      instance.ctselectSubscription = null;
    }

    if (!crosstalkOptions.group) {
      $table[0].ctfilter = null;
      $table[0].ctselect = null;
    } else {
      var key = crosstalkOptions.key;
      function keysToMatches(keys) {
        if (!keys) {
          return null;
        } else {
          var selectedKeys = {};
          for (var i = 0; i < keys.length; i++) {
            selectedKeys[keys[i]] = true;
          }
          var matches = {};
          for (var j = 0; j < key.length; j++) {
            if (selectedKeys[key[j]])
              matches[j] = true;
          }
          return matches;
        }
      }

      function applyCrosstalkFilter(e) {
        $table[0].ctfilter = keysToMatches(e.value);
        table.draw();
      }
      instance.ctfilterSubscription = instance.ctfilterHandle.on("change", applyCrosstalkFilter);
      applyCrosstalkFilter({value: instance.ctfilterHandle.filteredKeys});

      function applyCrosstalkSelection(e) {
        if (e.sender !== instance.ctselectHandle) {
          table
            .rows('.' + selClass, {search: 'applied'})
            .nodes()
            .to$()
            .removeClass(selClass);
          if (selectedRows)
            changeInput('rows_selected', selectedRows(), void 0, true);
        }

        if (e.sender !== instance.ctselectHandle && e.value && e.value.length) {
          var matches = keysToMatches(e.value);

          // persistent selection with plotly (& leaflet)
          var ctOpts = crosstalk.var("plotlyCrosstalkOpts").get() || {};
          if (ctOpts.persistent === true) {
            var matches = $.extend(matches, $table[0].ctselect);
          }

          $table[0].ctselect = matches;
          table.draw();
        } else {
          if ($table[0].ctselect) {
            $table[0].ctselect = null;
            table.draw();
          }
        }
      }
      instance.ctselectSubscription = instance.ctselectHandle.on("change", applyCrosstalkSelection);
      // TODO: This next line doesn't seem to work when renderDataTable is used
      applyCrosstalkSelection({value: instance.ctselectHandle.value});
    }

    var inArray = function(val, array) {
      return $.inArray(val, $.makeArray(array)) > -1;
    };

    // search the i-th column
    var searchColumn = function(i, value) {
      var regex = false, ci = true;
      if (options.search) {
        regex = options.search.regex,
        ci = options.search.caseInsensitive !== false;
      }
      return table.column(i).search(value, regex, !regex, ci);
    };

    if (data.filter !== 'none') {

      filterRow.each(function(i, td) {

        var $td = $(td), type = $td.data('type'), filter;
        var $input = $td.children('div').first().children('input');
        var disabled = $input.prop('disabled');
        var searchable = table.settings()[0].aoColumns[i].bSearchable;
        $input.prop('disabled', !searchable || disabled);
        $input.data('searchable', searchable); // for updating later
        $input.on('input blur', function() {
          $input.next('span').toggle(Boolean($input.val()));
        });
        // Bootstrap sets pointer-events to none and we won't be able to click
        // the clear button
        $input.next('span').css('pointer-events', 'auto').hide().click(function() {
          $(this).hide().prev('input').val('').trigger('input').focus();
        });
        var searchCol;  // search string for this column
        if (searchCols && searchCols[i]) {
          searchCol = searchCols[i];
          $input.val(searchCol).trigger('input');
        }
        var $x = $td.children('div').last();

        // remove the overflow: hidden attribute of the scrollHead
        // (otherwise the scrolling table body obscures the filters)
        // The workaround and the discussion from
        // https://github.com/rstudio/DT/issues/554#issuecomment-518007347
        // Otherwise the filter selection will not be anchored to the values
        // when the columns number is many and scrollX is enabled.
        var scrollHead = $(el).find('.dataTables_scrollHead,.dataTables_scrollFoot');
        var cssOverflowHead = scrollHead.css('overflow');
        var scrollBody = $(el).find('.dataTables_scrollBody');
        var cssOverflowBody = scrollBody.css('overflow');
        var scrollTable = $(el).find('.dataTables_scroll');
        var cssOverflowTable = scrollTable.css('overflow');
        if (cssOverflowHead === 'hidden') {
          $x.on('show hide', function(e) {
            if (e.type === 'show') {
              scrollHead.css('overflow', 'visible');
              scrollBody.css('overflow', 'visible');
              scrollTable.css('overflow-x', 'scroll');
            } else {
              scrollHead.css('overflow', cssOverflowHead);
              scrollBody.css('overflow', cssOverflowBody);
              scrollTable.css('overflow-x', cssOverflowTable);
            }
          });
          $x.css('z-index', 25);
        }

        if (inArray(type, ['factor', 'logical'])) {
          $input.on({
            click: function() {
              $input.parent().hide(); $x.show().trigger('show'); filter[0].selectize.focus();
            },
            input: function() {
              if ($input.val() === '') filter[0].selectize.setValue([]);
            }
          });
          var $input2 = $x.children('select');
          filter = $input2.selectize({
            options: $input2.data('options').map(function(v, i) {
              return ({text: v, value: v});
            }),
            plugins: ['remove_button'],
            hideSelected: true,
            onChange: function(value) {
              if (value === null) value = []; // compatibility with jQuery 3.0
              $input.val(value.length ? JSON.stringify(value) : '');
              if (value.length) $input.trigger('input');
              $input.attr('title', $input.val());
              if (server) {
                table.column(i).search(value.length ? JSON.stringify(value) : '').draw();
                return;
              }
              // turn off filter if nothing selected
              $td.data('filter', value.length > 0);
              table.draw();  // redraw table, and filters will be applied
            }
          });
          if (searchCol) filter[0].selectize.setValue(JSON.parse(searchCol));
          filter[0].selectize.on('blur', function() {
            $x.hide().trigger('hide'); $input.parent().show(); $input.trigger('blur');
          });
          filter.next('div').css('margin-bottom', 'auto');
        } else if (type === 'character') {
          var fun = function() {
            searchColumn(i, $input.val()).draw();
          };
          if (server) {
            fun = $.fn.dataTable.util.throttle(fun, options.searchDelay);
          }
          $input.on('input', fun);
        } else if (inArray(type, ['number', 'integer', 'date', 'time'])) {
          var $x0 = $x;
          $x = $x0.children('div').first();
          $x0.css({
            'background-color': '#fff',
            'border': '1px #ddd solid',
            'border-radius': '4px',
            'padding': data.vertical ? '35px 20px': '20px 20px 10px 20px'
          });
          var $spans = $x0.children('span').css({
            'margin-top': data.vertical ? '0' : '10px',
            'white-space': 'nowrap'
          });
          var $span1 = $spans.first(), $span2 = $spans.last();
          var r1 = +$x.data('min'), r2 = +$x.data('max');
          // when the numbers are too small or have many decimal places, the
          // slider may have numeric precision problems (#150)
          var scale = Math.pow(10, Math.max(0, +$x.data('scale') || 0));
          r1 = Math.round(r1 * scale); r2 = Math.round(r2 * scale);
          var scaleBack = function(x, scale) {
            if (scale === 1) return x;
            var d = Math.round(Math.log(scale) / Math.log(10));
            // to avoid problems like 3.423/100 -> 0.034230000000000003
            return (x / scale).toFixed(d);
          };
          var slider_min = function() {
            return filter.noUiSlider('options').range.min;
          };
          var slider_max = function() {
            return filter.noUiSlider('options').range.max;
          };
          $input.on({
            focus: function() {
              $x0.show().trigger('show');
              // first, make sure the slider div leaves at least 20px between
              // the two (slider value) span's
              $x0.width(Math.max(160, $span1.outerWidth() + $span2.outerWidth() + 20));
              // then, if the input is really wide or slider is vertical,
              // make the slider the same width as the input
              if ($x0.outerWidth() < $input.outerWidth() || data.vertical) {
                $x0.outerWidth($input.outerWidth());
              }
              // make sure the slider div does not reach beyond the right margin
              if ($(window).width() < $x0.offset().left + $x0.width()) {
                $x0.offset({
                  'left': $input.offset().left + $input.outerWidth() - $x0.outerWidth()
                });
              }
            },
            blur: function() {
              $x0.hide().trigger('hide');
            },
            input: function() {
              if ($input.val() === '') filter.val([slider_min(), slider_max()]);
            },
            change: function() {
              var v = $input.val().replace(/\s/g, '');
              if (v === '') return;
              v = v.split('...');
              if (v.length !== 2) {
                $input.parent().addClass('has-error');
                return;
              }
              if (v[0] === '') v[0] = slider_min();
              if (v[1] === '') v[1] = slider_max();
              $input.parent().removeClass('has-error');
              // treat date as UTC time at midnight
              var strTime = function(x) {
                var s = type === 'date' ? 'T00:00:00Z' : '';
                var t = new Date(x + s).getTime();
                // add 10 minutes to date since it does not hurt the date, and
                // it helps avoid the tricky floating point arithmetic problems,
                // e.g. sometimes the date may be a few milliseconds earlier
                // than the midnight due to precision problems in noUiSlider
                return type === 'date' ? t + 3600000 : t;
              };
              if (inArray(type, ['date', 'time'])) {
                v[0] = strTime(v[0]);
                v[1] = strTime(v[1]);
              }
              if (v[0] != slider_min()) v[0] *= scale;
              if (v[1] != slider_max()) v[1] *= scale;
              filter.val(v);
            }
          });
          var formatDate = function(d, isoFmt) {
            d = scaleBack(d, scale);
            if (type === 'number') return d;
            if (type === 'integer') return parseInt(d);
            var x = new Date(+d);
            var fmt = ('filterDateFmt' in data) ? data.filterDateFmt[i] : undefined;
            if (fmt !== undefined && isoFmt === false) return x[fmt.method].apply(x, fmt.params);
            if (type === 'date') {
              var pad0 = function(x) {
                return ('0' + x).substr(-2, 2);
              };
              return x.getUTCFullYear() + '-' + pad0(1 + x.getUTCMonth())
                      + '-' + pad0(x.getUTCDate());
            } else {
              return x.toISOString();
            }
          };
          var opts = type === 'date' ? { step: 60 * 60 * 1000 } :
                     type === 'integer' ? { step: 1 } : {};

          opts.orientation = data.vertical ? 'vertical': 'horizontal';
          opts.direction = data.vertical ? 'rtl': 'ltr';

          filter = $x.noUiSlider($.extend({
            start: [r1, r2],
            range: {min: r1, max: r2},
            connect: true
          }, opts));
          if (scale > 1) (function() {
            var t1 = r1, t2 = r2;
            var val = filter.val();
            while (val[0] > r1 || val[1] < r2) {
              if (val[0] > r1) {
                t1 -= val[0] - r1;
              }
              if (val[1] < r2) {
                t2 += r2 - val[1];
              }
              filter = $x.noUiSlider($.extend({
                start: [t1, t2],
                range: {min: t1, max: t2},
                connect: true
              }, opts), true);
              val = filter.val();
            }
            r1  = t1; r2 = t2;
          })();
          var updateSliderText = function(v1, v2) {
            $span1.text(formatDate(v1, false)); $span2.text(formatDate(v2, false));
          };
          updateSliderText(r1, r2);
          var updateSlider = function(e) {
            var val = filter.val();
            // turn off filter if in full range
            $td.data('filter', val[0] > slider_min() || val[1] < slider_max());
            var v1 = formatDate(val[0]), v2 = formatDate(val[1]), ival;
            if ($td.data('filter')) {
              ival = v1 + ' ... ' + v2;
              $input.attr('title', ival).val(ival).trigger('input');
            } else {
              $input.attr('title', '').val('');
            }
            updateSliderText(val[0], val[1]);
            if (e.type === 'slide') return;  // no searching when sliding only
            if (server) {
              table.column(i).search($td.data('filter') ? ival : '').draw();
              return;
            }
            table.draw();
          };
          filter.on({
            set: updateSlider,
            slide: updateSlider
          });
        }

        // server-side processing will be handled by R (or whatever server
        // language you use); the following code is only needed for client-side
        // processing
        if (server) {
          // if a search string has been pre-set, search now
          if (searchCol) searchColumn(i, searchCol).draw();
          return;
        }

        var customFilter = function(settings, data, dataIndex) {
          // there is no way to attach a search function to a specific table,
          // and we need to make sure a global search function is not applied to
          // all tables (i.e. a range filter in a previous table should not be
          // applied to the current table); we use the settings object to
          // determine if we want to perform searching on the current table,
          // since settings.sTableId will be different to different tables
          if (table.settings()[0] !== settings) return true;
          // no filter on this column or no need to filter this column
          if (typeof filter === 'undefined' || !$td.data('filter')) return true;

          var r = filter.val(), v, r0, r1;
          var i_data = function(i) {
            if (!colReorderEnabled()) return i;
            var order = table.colReorder.order(), k;
            for (k = 0; k < order.length; ++k) if (order[k] === i) return k;
            return i; // in theory it will never be here...
          }
          v = data[i_data(i)];
          if (type === 'number' || type === 'integer') {
            v = parseFloat(v);
            // how to handle NaN? currently exclude these rows
            if (isNaN(v)) return(false);
            r0 = parseFloat(scaleBack(r[0], scale))
            r1 = parseFloat(scaleBack(r[1], scale));
            if (v >= r0 && v <= r1) return true;
          } else if (type === 'date' || type === 'time') {
            v = new Date(v);
            r0 = new Date(r[0] / scale); r1 = new Date(r[1] / scale);
            if (v >= r0 && v <= r1) return true;
          } else if (type === 'factor') {
            if (r.length === 0 || inArray(v, r)) return true;
          } else if (type === 'logical') {
            if (r.length === 0) return true;
            if (inArray(v === '' ? 'na' : v, r)) return true;
          }
          return false;
        };

        $.fn.dataTable.ext.search.push(customFilter);

        // search for the preset search strings if it is non-empty
        if (searchCol) {
          if (inArray(type, ['factor', 'logical'])) {
            filter[0].selectize.setValue(JSON.parse(searchCol));
          } else if (type === 'character') {
            $input.trigger('input');
          } else if (inArray(type, ['number', 'integer', 'date', 'time'])) {
            $input.trigger('change');
          }
        }

      });

    }

    // highlight search keywords
    var highlight = function() {
      var body = $(table.table().body());
      // removing the old highlighting first
      body.unhighlight();

      // don't highlight the "not found" row, so we get the rows using the api
      if (table.rows({ filter: 'applied' }).data().length === 0) return;
      // highlight global search keywords
      body.highlight($.trim(table.search()).split(/\s+/));
      // then highlight keywords from individual column filters
      if (filterRow) filterRow.each(function(i, td) {
        var $td = $(td), type = $td.data('type');
        if (type !== 'character') return;
        var $input = $td.children('div').first().children('input');
        var column = table.column(i).nodes().to$(),
            val = $.trim($input.val());
        if (type !== 'character' || val === '') return;
        column.highlight(val.split(/\s+/));
      });
    };

    if (options.searchHighlight) {
      table
      .on('draw.dt.dth column-visibility.dt.dth column-reorder.dt.dth', highlight)
      .on('destroy', function() {
        // remove event handler
        table.off('draw.dt.dth column-visibility.dt.dth column-reorder.dt.dth');
      });

      // Set the option for escaping regex characters in our search string.  This will be used
      // for all future matching.
      jQuery.fn.highlight.options.escapeRegex = (!options.search || !options.search.regex);

      // initial highlight for state saved conditions and initial states
      highlight();
    }

    // run the callback function on the table instance
    if (typeof data.callback === 'function') data.callback(table);

    // double click to edit the cell, row, column, or all cells
    if (data.editable) table.on('dblclick.dt', 'tbody td', function(e) {
      // only bring up the editor when the cell itself is dbclicked, and ignore
      // other dbclick events bubbled up (e.g. from the <input>)
      if (e.target !== this) return;
      var target = [], immediate = false;
      switch (data.editable.target) {
        case 'cell':
          target = [this];
          immediate = true;  // edit will take effect immediately
          break;
        case 'row':
          target = table.cells(table.cell(this).index().row, '*').nodes();
          break;
        case 'column':
          target = table.cells('*', table.cell(this).index().column).nodes();
          break;
        case 'all':
          target = table.cells().nodes();
          break;
        default:
          throw 'The editable parameter must be "cell", "row", "column", or "all"';
      }
      var disableCols = data.editable.disable ? data.editable.disable.columns : null;
      var numericCols = data.editable.numeric;
      var areaCols = data.editable.area;
      var dateCols = data.editable.date;
      for (var i = 0; i < target.length; i++) {
        (function(cell, current) {
          var $cell = $(cell), html = $cell.html();
          var _cell = table.cell(cell), value = _cell.data(), index = _cell.index().column;
          var $input;
          if (inArray(index, numericCols)) {
            $input = $('<input type="number">');
          } else if (inArray(index, areaCols)) {
            $input = $('<textarea></textarea>');
          } else if (inArray(index, dateCols)) {
            $input = $('<input type="date">');
          } else {
            $input = $('<input type="text">');
          }
          if (!immediate) {
            $cell.data('input', $input).data('html', html);
            $input.attr('title', 'Hit Ctrl+Enter to finish editing, or Esc to cancel');
          }
          $input.val(value);
          if (inArray(index, disableCols)) {
            $input.attr('readonly', '').css('filter', 'invert(25%)');
          }
          $cell.empty().append($input);
          if (cell === current) $input.focus();
          $input.css('width', '100%');

          if (immediate) $input.on('blur', function(e) {
            var valueNew = $input.val();
            if (valueNew !== value) {
              _cell.data(valueNew);
              if (HTMLWidgets.shinyMode) {
                changeInput('cell_edit', [cellInfo(cell)], 'DT.cellInfo', null, {priority: 'event'});
              }
              // for server-side processing, users have to call replaceData() to update the table
              if (!server) table.draw(false);
            } else {
              $cell.html(html);
            }
          }).on('keyup', function(e) {
            // hit Escape to cancel editing
            if (e.keyCode === 27) $input.trigger('blur');
          });

          // bulk edit (row, column, or all)
          if (!immediate) $input.on('keyup', function(e) {
            var removeInput = function($cell, restore) {
              $cell.data('input').remove();
              if (restore) $cell.html($cell.data('html'));
            }
            if (e.keyCode === 27) {
              for (var i = 0; i < target.length; i++) {
                removeInput($(target[i]), true);
              }
            } else if (e.keyCode === 13 && e.ctrlKey) {
              // Ctrl + Enter
              var cell, $cell, _cell, cellData = [];
              for (var i = 0; i < target.length; i++) {
                cell = target[i]; $cell = $(cell); _cell = table.cell(cell);
                _cell.data($cell.data('input').val());
                HTMLWidgets.shinyMode && cellData.push(cellInfo(cell));
                removeInput($cell, false);
              }
              if (HTMLWidgets.shinyMode) {
                changeInput('cell_edit', cellData, 'DT.cellInfo', null, {priority: "event"});
              }
              if (!server) table.draw(false);
            }
          });
        })(target[i], this);
      }
    });

    // interaction with shiny
    if (!HTMLWidgets.shinyMode && !crosstalkOptions.group) return;

    var methods = {};
    var shinyData = {};

    methods.updateCaption = function(caption) {
      if (!caption) return;
      $table.children('caption').replaceWith(caption);
    }

    // register clear functions to remove input values when the table is removed
    instance.clearInputs = {};

    var changeInput = function(id, value, type, noCrosstalk, opts) {
      var event = id;
      id = el.id + '_' + id;
      if (type) id = id + ':' + type;
      // do not update if the new value is the same as old value
      if (event !== 'cell_edit' && !/_clicked$/.test(event) && shinyData.hasOwnProperty(id) && shinyData[id] === JSON.stringify(value))
        return;
      shinyData[id] = JSON.stringify(value);
      if (HTMLWidgets.shinyMode && Shiny.setInputValue) {
        Shiny.setInputValue(id, value, opts);
        if (!instance.clearInputs[id]) instance.clearInputs[id] = function() {
          Shiny.setInputValue(id, null);
        }
      }

      // HACK
      if (event === "rows_selected" && !noCrosstalk) {
        if (crosstalkOptions.group) {
          var keys = crosstalkOptions.key;
          var selectedKeys = null;
          if (value) {
            selectedKeys = [];
            for (var i = 0; i < value.length; i++) {
              // The value array's contents use 1-based row numbers, so we must
              // convert to 0-based before indexing into the keys array.
              selectedKeys.push(keys[value[i] - 1]);
            }
          }
          instance.ctselectHandle.set(selectedKeys);
        }
      }
    };

    var addOne = function(x) {
      return x.map(function(i) { return 1 + i; });
    };

    var unique = function(x) {
      var ux = [];
      $.each(x, function(i, el){
        if ($.inArray(el, ux) === -1) ux.push(el);
      });
      return ux;
    }

    // change the row index of a cell
    var tweakCellIndex = function(cell) {
      var info = cell.index();
      // some cell may not be valid. e.g, #759
      // when using the RowGroup extension, datatables will
      // generate the row label and the cells are not part of
      // the data thus contain no row/col info
      if (info === undefined)
        return {row: null, col: null};
      if (server) {
        info.row = DT_rows_current[info.row];
      } else {
        info.row += 1;
      }
      return {row: info.row, col: info.column};
    }

    var cleanSelectedValues = function() {
      changeInput('rows_selected', []);
      changeInput('columns_selected', []);
      changeInput('cells_selected', transposeArray2D([]), 'shiny.matrix');
    }
    // #828 we should clean the selection on the server-side when the table reloads
    cleanSelectedValues();

    // a flag to indicates if select extension is initialized or not
    var flagSelectExt = table.settings()[0]._select !== undefined;
    // the Select extension should only be used in the client mode and
    // when the selection.mode is set to none
    if (data.selection.mode === 'none' && !server && flagSelectExt) {
      var updateRowsSelected = function() {
        var rows = table.rows({selected: true});
        var selected = [];
        $.each(rows.indexes().toArray(), function(i, v) {
          selected.push(v + 1);
        });
        changeInput('rows_selected', selected);
      }
      var updateColsSelected = function() {
        var columns = table.columns({selected: true});
        changeInput('columns_selected', columns.indexes().toArray());
      }
      var updateCellsSelected = function() {
        var cells = table.cells({selected: true});
        var selected = [];
        cells.every(function() {
          var row = this.index().row;
          var col = this.index().column;
          selected = selected.concat([[row + 1, col]]);
        });
        changeInput('cells_selected', transposeArray2D(selected), 'shiny.matrix');
      }
      table.on('select deselect', function(e, dt, type, indexes) {
        updateRowsSelected();
        updateColsSelected();
        updateCellsSelected();
      })
    }

    var selMode = data.selection.mode, selTarget = data.selection.target;
    var selDisable = data.selection.selectable === false;
    if (inArray(selMode, ['single', 'multiple'])) {
      var selClass = inArray(data.style, ['bootstrap', 'bootstrap4']) ? 'active' : 'selected';
      // selected1: row indices; selected2: column indices
      var initSel = function(x) {
        if (x === null || typeof x === 'boolean' || selTarget === 'cell') {
          return {rows: [], cols: []};
        } else if (selTarget === 'row') {
          return {rows: $.makeArray(x), cols: []};
        } else if (selTarget === 'column') {
          return {rows: [], cols: $.makeArray(x)};
        } else if (selTarget === 'row+column') {
          return {rows: $.makeArray(x.rows), cols: $.makeArray(x.cols)};
        }
      }
      var selected = data.selection.selected;
      var selected1 = initSel(selected).rows, selected2 = initSel(selected).cols;
      // selectable should contain either all positive or all non-positive values, not both
      // positive values indicate "selectable" while non-positive values means "nonselectable"
      // the assertion is performed on R side. (only column indicides could be zero which indicates
      // the row name)
      var selectable = data.selection.selectable;
      var selectable1 = initSel(selectable).rows, selectable2 = initSel(selectable).cols;

      // After users reorder the rows or filter the table, we cannot use the table index
      // directly. Instead, we need this function to find out the rows between the two clicks.
      // If user filter the table again between the start click and the end click, the behavior
      // would be undefined, but it should not be a problem.
      var shiftSelRowsIndex = function(start, end) {
        var indexes = server ? DT_rows_all : table.rows({ search: 'applied' }).indexes().toArray();
        start = indexes.indexOf(start); end = indexes.indexOf(end);
        // if start is larger than end, we need to swap
        if (start > end) {
          var tmp = end; end = start; start = tmp;
        }
        return indexes.slice(start, end + 1);
      }

      var serverRowIndex = function(clientRowIndex) {
        return server ? DT_rows_current[clientRowIndex] : clientRowIndex + 1;
      }

      // row, column, or cell selection
      var lastClickedRow;
      if (inArray(selTarget, ['row', 'row+column'])) {
        // Get the current selected rows. It will also
        // update the selected1's value based on the current row selection state
        // Note we can't put this function inside selectRows() directly,
        // the reason is method.selectRows() will override selected1's value but this
        // function will add rows to selected1 (keep the existing selection), which is
        // inconsistent with column and cell selection.
        var selectedRows = function() {
          var rows = table.rows('.' + selClass);
          var idx = rows.indexes().toArray();
          if (!server) {
            selected1 = addOne(idx);
            return selected1;
          }
          idx = idx.map(function(i) {
            return DT_rows_current[i];
          });
          selected1 = selMode === 'multiple' ? unique(selected1.concat(idx)) : idx;
          return selected1;
        }
        // Change selected1's value based on selectable1, then refresh the row state
        var onlyKeepSelectableRows = function() {
          if (selDisable) { // users can't select; useful when only want backend select
            selected1 = [];
            return;
          }
          if (selectable1.length === 0) return;
          var nonselectable = selectable1[0] <= 0;
          if (nonselectable) {
            // should make selectable1 positive
            selected1 = $(selected1).not(selectable1.map(function(i) { return -i; })).get();
          } else {
            selected1 = $(selected1).filter(selectable1).get();
          }
        }
        // Change selected1's value based on selectable1, then
        // refresh the row selection state according to values in selected1
        var selectRows = function(ignoreSelectable) {
          if (!ignoreSelectable) onlyKeepSelectableRows();
          table.$('tr.' + selClass).removeClass(selClass);
          if (selected1.length === 0) return;
          if (server) {
            table.rows({page: 'current'}).every(function() {
              if (inArray(DT_rows_current[this.index()], selected1)) {
                $(this.node()).addClass(selClass);
              }
            });
          } else {
            var selected0 = selected1.map(function(i) { return i - 1; });
            $(table.rows(selected0).nodes()).addClass(selClass);
          }
        }
        table.on('mousedown.dt', 'tbody tr', function(e) {
          var $this = $(this), thisRow = table.row(this);
          if (selMode === 'multiple') {
            if (e.shiftKey && lastClickedRow !== undefined) {
              // select or de-select depends on the last clicked row's status
              var flagSel = !$this.hasClass(selClass);
              var crtClickedRow = serverRowIndex(thisRow.index());
              if (server) {
                var rowsIndex = shiftSelRowsIndex(lastClickedRow, crtClickedRow);
                // update current page's selClass
                rowsIndex.map(function(i) {
                  var rowIndex = DT_rows_current.indexOf(i);
                  if (rowIndex >= 0) {
                    var row = table.row(rowIndex).nodes().to$();
                    var flagRowSel = !row.hasClass(selClass);
                    if (flagSel === flagRowSel) row.toggleClass(selClass);
                  }
                });
                // update selected1
                if (flagSel) {
                  selected1 = unique(selected1.concat(rowsIndex));
                } else {
                  selected1 = selected1.filter(function(index) {
                    return !inArray(index, rowsIndex);
                  });
                }
              } else {
                // js starts from 0
                shiftSelRowsIndex(lastClickedRow - 1, crtClickedRow - 1).map(function(value) {
                  var row = table.row(value).nodes().to$();
                  var flagRowSel = !row.hasClass(selClass);
                  if (flagSel === flagRowSel) row.toggleClass(selClass);
                });
              }
              e.preventDefault();
            } else {
              $this.toggleClass(selClass);
            }
          } else {
            if ($this.hasClass(selClass)) {
              $this.removeClass(selClass);
            } else {
              table.$('tr.' + selClass).removeClass(selClass);
              $this.addClass(selClass);
            }
          }
          if (server && !$this.hasClass(selClass)) {
            var id = DT_rows_current[thisRow.index()];
            // remove id from selected1 since its class .selected has been removed
            if (inArray(id, selected1)) selected1.splice($.inArray(id, selected1), 1);
          }
          selectedRows(); // update selected1's value based on selClass
          selectRows(false); // only keep the selectable rows
          changeInput('rows_selected', selected1);
          changeInput('row_last_clicked', serverRowIndex(thisRow.index()), null, null, {priority: 'event'});
          lastClickedRow = serverRowIndex(thisRow.index());
        });
        selectRows(false);  // in case users have specified pre-selected rows
        // restore selected rows after the table is redrawn (e.g. sort/search/page);
        // client-side tables will preserve the selections automatically; for
        // server-side tables, we have to *real* row indices are in `selected1`
        changeInput('rows_selected', selected1);
        if (server) table.on('draw.dt', function(e) { selectRows(false); });
        methods.selectRows = function(selected, ignoreSelectable) {
          selected1 = $.makeArray(selected);
          selectRows(ignoreSelectable);
          changeInput('rows_selected', selected1);
        }
      }

      if (inArray(selTarget, ['column', 'row+column'])) {
        if (selTarget === 'row+column') {
          $(table.columns().footer()).css('cursor', 'pointer');
        }
        // update selected2's value based on selectable2
        var onlyKeepSelectableCols = function() {
          if (selDisable) { // users can't select; useful when only want backend select
            selected2 = [];
            return;
          }
          if (selectable2.length === 0) return;
          var nonselectable = selectable2[0] <= 0;
          if (nonselectable) {
            // need to make selectable2 positive
            selected2 = $(selected2).not(selectable2.map(function(i) { return -i; })).get();
          } else {
            selected2 = $(selected2).filter(selectable2).get();
          }
        }
        // update selected2 and then
        // refresh the col selection state according to values in selected2
        var selectCols = function(ignoreSelectable) {
          if (!ignoreSelectable) onlyKeepSelectableCols();
          // if selected2 is not a valide index (e.g., larger than the column number)
          // table.columns(selected2) will fail and result in a blank table
          // this is different from the table.rows(), where the out-of-range indexes
          // doesn't affect at all
          selected2 = $(selected2).filter(table.columns().indexes()).get();
          table.columns().nodes().flatten().to$().removeClass(selClass);
          if (selected2.length > 0)
            table.columns(selected2).nodes().flatten().to$().addClass(selClass);
        }
        var callback = function() {
          var colIdx = selTarget === 'column' ? table.cell(this).index().column :
              $.inArray(this, table.columns().footer()),
              thisCol = $(table.column(colIdx).nodes());
          if (colIdx === -1) return;
          if (thisCol.hasClass(selClass)) {
            thisCol.removeClass(selClass);
            selected2.splice($.inArray(colIdx, selected2), 1);
          } else {
            if (selMode === 'single') $(table.cells().nodes()).removeClass(selClass);
            thisCol.addClass(selClass);
            selected2 = selMode === 'single' ? [colIdx] : unique(selected2.concat([colIdx]));
          }
          selectCols(false); // update selected2 based on selectable
          changeInput('columns_selected', selected2);
        }
        if (selTarget === 'column') {
          $(table.table().body()).on('click.dt', 'td', callback);
        } else {
          $(table.table().footer()).on('click.dt', 'tr th', callback);
        }
        selectCols(false);  // in case users have specified pre-selected columns
        changeInput('columns_selected', selected2);
        if (server) table.on('draw.dt', function(e) { selectCols(false); });
        methods.selectColumns = function(selected, ignoreSelectable) {
          selected2 = $.makeArray(selected);
          selectCols(ignoreSelectable);
          changeInput('columns_selected', selected2);
        }
      }

      if (selTarget === 'cell') {
        var selected3 = [], selectable3 = [];
        if (selected !== null) selected3 = selected;
        if (selectable !== null && typeof selectable !== 'boolean') selectable3 = selectable;
        var findIndex = function(ij, sel) {
          for (var i = 0; i < sel.length; i++) {
            if (ij[0] === sel[i][0] && ij[1] === sel[i][1]) return i;
          }
          return -1;
        }
         // Change selected3's value based on selectable3, then refresh the cell state
        var onlyKeepSelectableCells = function() {
          if (selDisable) { // users can't select; useful when only want backend select
            selected3 = [];
            return;
          }
          if (selectable3.length === 0) return;
          var nonselectable = selectable3[0][0] <= 0;
          var out = [];
          if (nonselectable) {
            selected3.map(function(ij) {
              // should make selectable3 positive
              if (findIndex([-ij[0], -ij[1]], selectable3) === -1) { out.push(ij); }
            });
          } else {
            selected3.map(function(ij) {
              if (findIndex(ij, selectable3) > -1) { out.push(ij); }
            });
          }
          selected3 = out;
        }
        // Change selected3's value based on selectable3, then
        // refresh the cell selection state according to values in selected3
        var selectCells = function(ignoreSelectable) {
          if (!ignoreSelectable) onlyKeepSelectableCells();
          table.$('td.' + selClass).removeClass(selClass);
          if (selected3.length === 0) return;
          if (server) {
            table.cells({page: 'current'}).every(function() {
              var info = tweakCellIndex(this);
              if (findIndex([info.row, info.col], selected3) > -1)
                $(this.node()).addClass(selClass);
            });
          } else {
            selected3.map(function(ij) {
              $(table.cell(ij[0] - 1, ij[1]).node()).addClass(selClass);
            });
          }
        };
        table.on('click.dt', 'tbody td', function() {
          var $this = $(this), info = tweakCellIndex(table.cell(this));
          if ($this.hasClass(selClass)) {
            $this.removeClass(selClass);
            selected3.splice(findIndex([info.row, info.col], selected3), 1);
          } else {
            if (selMode === 'single') $(table.cells().nodes()).removeClass(selClass);
            $this.addClass(selClass);
            selected3 = selMode === 'single' ? [[info.row, info.col]] :
              unique(selected3.concat([[info.row, info.col]]));
          }
          selectCells(false); // must call this to update selected3 based on selectable3
          changeInput('cells_selected', transposeArray2D(selected3), 'shiny.matrix');
        });
        selectCells(false);  // in case users have specified pre-selected columns
        changeInput('cells_selected', transposeArray2D(selected3), 'shiny.matrix');

        if (server) table.on('draw.dt', function(e) { selectCells(false); });
        methods.selectCells = function(selected, ignoreSelectable) {
          selected3 = selected ? selected : [];
          selectCells(ignoreSelectable);
          changeInput('cells_selected', transposeArray2D(selected3), 'shiny.matrix');
        }
      }
    }

    // expose some table info to Shiny
    var updateTableInfo = function(e, settings) {
      // TODO: is anyone interested in the page info?
      // changeInput('page_info', table.page.info());
      var updateRowInfo = function(id, modifier) {
        var idx;
        if (server) {
          idx = modifier.page === 'current' ? DT_rows_current : DT_rows_all;
        } else {
          var rows = table.rows($.extend({
            search: 'applied',
            page: 'all'
          }, modifier));
          idx = addOne(rows.indexes().toArray());
        }
        changeInput('rows' + '_' + id, idx);
      };
      updateRowInfo('current', {page: 'current'});
      updateRowInfo('all', {});
    }
    table.on('draw.dt', updateTableInfo);
    updateTableInfo();

    // state info
    table.on('draw.dt column-visibility.dt', function() {
      changeInput('state', table.state());
    });
    changeInput('state', table.state());

    // search info
    var updateSearchInfo = function() {
      changeInput('search', table.search());
      if (filterRow) changeInput('search_columns', filterRow.toArray().map(function(td) {
        return $(td).find('input').first().val();
      }));
    }
    table.on('draw.dt', updateSearchInfo);
    updateSearchInfo();

    var cellInfo = function(thiz) {
      var info = tweakCellIndex(table.cell(thiz));
      info.value = table.cell(thiz).data();
      return info;
    }
    // the current cell clicked on
    table.on('click.dt', 'tbody td', function() {
      changeInput('cell_clicked', cellInfo(this), null, null, {priority: 'event'});
    })
    changeInput('cell_clicked', {});

    // do not trigger table selection when clicking on links unless they have classes
    table.on('click.dt', 'tbody td a', function(e) {
      if (this.className === '') e.stopPropagation();
    });

    methods.addRow = function(data, rowname, resetPaging) {
      var n = table.columns().indexes().length, d = n - data.length;
      if (d === 1) {
        data = rowname.concat(data)
      } else if (d !== 0) {
        console.log(data);
        console.log(table.columns().indexes());
        throw 'New data must be of the same length as current data (' + n + ')';
      };
      table.row.add(data).draw(resetPaging);
    }

    methods.updateSearch = function(keywords) {
      if (keywords.global !== null)
        $(table.table().container()).find('input[type=search]').first()
             .val(keywords.global).trigger('input');
      var columns = keywords.columns;
      if (!filterRow || columns === null) return;
      filterRow.toArray().map(function(td, i) {
        var v = typeof columns === 'string' ? columns : columns[i];
        if (typeof v === 'undefined') {
          console.log('The search keyword for column ' + i + ' is undefined')
          return;
        }
        $(td).find('input').first().val(v);
        searchColumn(i, v);
      });
      table.draw();
    }

    methods.hideCols = function(hide, reset) {
      if (reset) table.columns().visible(true, false);
      table.columns(hide).visible(false);
    }

    methods.showCols = function(show, reset) {
      if (reset) table.columns().visible(false, false);
      table.columns(show).visible(true);
    }

    methods.colReorder = function(order, origOrder) {
      table.colReorder.order(order, origOrder);
    }

    methods.selectPage = function(page) {
      if (table.page.info().pages < page || page < 1) {
        throw 'Selected page is out of range';
      };
      table.page(page - 1).draw(false);
    }

    methods.reloadData = function(resetPaging, clearSelection) {
      // empty selections first if necessary
      if (methods.selectRows && inArray('row', clearSelection)) methods.selectRows([]);
      if (methods.selectColumns && inArray('column', clearSelection)) methods.selectColumns([]);
      if (methods.selectCells && inArray('cell', clearSelection)) methods.selectCells([]);
      table.ajax.reload(null, resetPaging);
    }

    // update table filters (set new limits of sliders)
    methods.updateFilters = function(newProps) {
      // loop through each filter in the filter row
      filterRow.each(function(i, td) {
        var k = i;
        if (filterRow.length > newProps.length) {
          if (i === 0) return;  // first column is row names
          k = i - 1;
        }
        // Update the filters to reflect the updated data.
        // Allow "falsy" (e.g. NULL) to signify a no-op.
        if (newProps[k]) {
          setFilterProps(td, newProps[k]);
        }
      });
    };

    table.shinyMethods = methods;
  },
  resize: function(el, width, height, instance) {
    if (instance.data) this.renderValue(el, instance.data, instance);

    // dynamically adjust height if fillContainer = TRUE
    if (instance.fillContainer)
      this.fillAvailableHeight(el, height);

    this.adjustWidth(el);
  },

  // dynamically set the scroll body to fill available height
  // (used with fillContainer = TRUE)
  fillAvailableHeight: function(el, availableHeight) {

    // see how much of the table is occupied by header/footer elements
    // and use that to compute a target scroll body height
    var dtWrapper = $(el).find('div.dataTables_wrapper');
    var dtScrollBody = $(el).find($('div.dataTables_scrollBody'));
    var framingHeight = dtWrapper.innerHeight() - dtScrollBody.innerHeight();
    var scrollBodyHeight = availableHeight - framingHeight;

    // we need to set `max-height` to none as datatables library now sets this
    // to a fixed height, disabling the ability to resize to fill the window,
    // as it will be set to a fixed 100px under such circumstances, e.g., RStudio IDE,
    // or FlexDashboard
    // see https://github.com/rstudio/DT/issues/951#issuecomment-1026464509
    dtScrollBody.css('max-height', 'none');
    // set the height
    dtScrollBody.height(scrollBodyHeight + 'px');
  },

  // adjust the width of columns; remove the hard-coded widths on table and the
  // scroll header when scrollX/Y are enabled
  adjustWidth: function(el) {
    var $el = $(el), table = $el.data('datatable');
    if (table) table.columns.adjust();
    $el.find('.dataTables_scrollHeadInner').css('width', '')
        .children('table').css('margin-left', '');
  }
});

  if (!HTMLWidgets.shinyMode) return;

  Shiny.addCustomMessageHandler('datatable-calls', function(data) {
    var id = data.id;
    var el = document.getElementById(id);
    var table = el ? $(el).data('datatable') : null;
    if (!table) {
      console.log("Couldn't find table with id " + id);
      return;
    }

    var methods = table.shinyMethods, call = data.call;
    if (methods[call.method]) {
      methods[call.method].apply(table, call.args);
    } else {
      console.log("Unknown method " + call.method);
    }
  });

})();
