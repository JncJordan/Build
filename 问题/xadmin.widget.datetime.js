;(function($){
    $.convert_format = function(format){
        var fields = {
            d: 'dd',
            H: 'hh',
            I: "HH",
            m: 'mm',
            M: 'MM',
            p: 'PM/AM',
            S: 'ss',
            w: 'w',
            y: 'yy',
            Y: 'yyyy',
            '%' : '%'
        };
        var result = '', i = 0;
        while (i < format.length) {
            if (format.charAt(i) === '%') {
                if(f = fields[format.charAt(i + 1)]){
                  result = result + f;
                }
                ++i;
            } else {
                result = result + format.charAt(i);
            }
            ++i;
        }
        return result;
    }

    $.date_local = {
      days: gettext("星期日 星期一 星期二 星期三 星期四 星期五 星期六 星期日").split(' '),
      daysShort: gettext("周日 周一 周二 周三 周四 周五 周六 周日").split(' '),
      daysMin: gettext("日 一 二 三 四 五 六 日").split(' '),
      months: gettext('一月 二月 三月 四月 五月 六月 七月 八月 九月 十月 十一月 十二月').split(' '),
      monthsShort: gettext("1月 2月 3月 4月 5月 6月 7月 8月 9月 10月 11月 12月").split(' '),
      today: gettext("今天"),
      date_string: gettext('%a %d %b %Y %T %Z'),
      ampm: gettext("AM PM").split(' '),
      ampmLower: gettext("am pm").split(' '),
      dateFormat: get_format('DATE_INPUT_FORMATS')[0],
      dateJSFormat: $.convert_format(get_format('DATE_INPUT_FORMATS')[0]),
      timeRepr: gettext('%T')
    }

    $.fn.datepicker.dates['xadmin'] = $.date_local;

    $.fn.exform.renders.push(function(f){
      f.find('.input-group.date input').each(function(e){
        var dp = $(this).datepicker({format: $.date_local.dateJSFormat, language: 'xadmin', todayBtn: "linked", autoclose: true})
          .data('datepicker');
        $(this).parent().find('button').click(function(e){
          dp.update(new Date());
        })
      })
      if($.fn.clockpicker){
        f.find('.input-group.bootstrap-clockpicker').each(function(e){
          var el = $(this).find('input');
          var tp = el.clockpicker({
              autoclose: true,
              'default': 'now'
          });

          $(this).find('button').click(function(e){
            var now = new Date()
              , value = now.getHours() + ':' + now.getMinutes();
            el.attr('value', value);
          })
        })
      }
      if($.fn.timepicker){
        f.find('.input-group.bootstrap-timepicker').each(function(e){
          var el = $(this).find('input');
          var value = el.val();
          var tp = el.timepicker({
            minuteStep: 1,
            showSeconds: true,
            showMeridian: false,
            defaultTime: false
          }).data('timepicker');
          $(this).find('button').click(function(e){
            tp.$element.val("");
            tp.setDefaultTime('current');
            tp.update();
          })
        })
      }
    });

})(jQuery)
