javascript:(function(){

    window.RGhasClass = function (el, theclass) {
        return (' ' + el.className + ' ').indexOf(' ' + theclass + ' ') > -1;
    };

    window.RGwidgetLoaded = function(inner, xhr) {
        window.RGajaxdata = JSON.parse(xhr.responseText);
        inner.className = 'rostergenius-inner';
        inner.innerHTML = window.formHTML;

        window.RGloadInput();

        document.querySelector('.rostergenius .dload').onclick = window.RGonDownloadClick;
        var inputs = document.querySelectorAll('.rostergenius .txt');

        for (var i = 0; i < inputs.length; i++) {
            inputs[i].oninput = window.RGsaveInput;
        };
    }

    window.RGsaveInput = function(ev) {
        try {
            // Safari will throw an exception if private browsing mode is on and LS is set
            localStorage.setItem('RG_field.' + this.getAttribute('id'), this.value);
        } catch(e) {}
    };

    window.RGloadInput = function() {
        for(var key in localStorage) {
            if(key.slice(0,8) == 'RG_field'){
                var fieldid = key.split('.')[1]
                var field = document.querySelector('.rostergenius #' + fieldid);
                field.value = localStorage.getItem(key);
            }
        }
    };

    window.RGonDownloadClick = function(){
        var d = document;
        var title = d.querySelector('.rostergenius #title').value;
        var location = d.querySelector('.rostergenius #location').value;
        var querystring = '';

        if(title.length > 0) {
            querystring += 'title=' + encodeURIComponent(title);
        }

        if(location.length > 0) {
            querystring += '&location=' + encodeURIComponent(location);
        }

        var dloadurl = 'http://rostergeni.us/download/' + window.RGajaxdata.accesstoken + '/?' + querystring;

        window.open(dloadurl);
        return false;
    };

    window.RGmain = function(d){
        var l = d.createElement('div');
        var inner = d.createElement('div');
        var t = d.createElement('a');
        var protocol = window.location.protocol;
        // protocol = 'http:';

        var body = d.querySelector('body');

        if(window.RGhasClass(body, 'rostergenius-loaded')) {
            alert('Bookmarklet already loaded.');
            return false;
        };

        body.className += ' rostergenius-loaded ';

        window.formHTML = '<div class="fields"><input class="txt" id="title" type="text" placeholder="Title"><input class="txt" id="location" type="text" placeholder="Location or store number"></div><a class="dload" href="">Download Roster</a>';
        var c = '.rostergenius{position:fixed;top:15px;right:15px;z-index:9999;width:350px;opacity:0;text-align:center;color:#fff;font:600 18px/1 "Helvetica Neue",sans-serif;box-sizing:border-box}.rostergenius *{box-sizing:border-box}.rostergenius-inner{background:-webkit-linear-gradient(#132333,#293846);box-shadow:0 0 7px -1px #52565A;border-radius:3px;width:100%;line-height:1.2;overflow:auto;padding:15px;box-sizing:border-box;-webkit-transition:all 250ms ease-in-out;-moz-transition:all 250ms ease-in-out;transition:all 250ms ease-in-out}.rostergenius-inner:hover{-webkit-transform:translateY(-2px);box-shadow:0 0 15px -2px #52565A}.rostergenius a:link,.rostergenius a:active,.rostergenius a:visited{color:inherit;text-decoration:none}.rostergenius a:hover{color:inherit;background:0 0;text-decoration:underline}.rostergenius .dload{display:block;width:50%;padding:8px 10px;float:right}.rostergenius .fields{width:50%;float:left;text-align:left}.rostergenius input.txt{width:100%;-webkit-appearance:none;border:1px solid #5E6B76;padding:5px;color:#fff;font-family:"Helvetica Neue";font-size:12px;background:#293744;border-radius:3px;outline:0}.rostergenius input.txt:focus{border-color:#9E9E9E}.animated{-webkit-animation-fill-mode:forwards;-moz-animation-fill-mode:forwards;-ms-animation-fill-mode:forwards;animation-fill-mode:forwards;-webkit-animation-duration:1s;-moz-animation-duration:1s;-ms-animation-duration:1s;animation-duration:1s}@-webkit-keyframes bounceInDown{0%{opacity:0;-webkit-transform:translateY(-2000px)}60%{opacity:1;-webkit-transform:translateY(30px)}80%{-webkit-transform:translateY(-10px)}100%{-webkit-transform:translateY(0);opacity:1}}@-moz-keyframes bounceInDown{0%{opacity:0;-moz-transform:translateY(-2000px)}60%{opacity:1;-moz-transform:translateY(30px)}80%{-moz-transform:translateY(-10px)}100%{-moz-transform:translateY(0);opacity:1}}@keyframes bounceInDown{0%{opacity:0;transform:translateY(-2000px)}60%{opacity:1;transform:translateY(30px)}80%{transform:translateY(-10px)}100%{transform:translateY(0);opacity:1}}.bounceInDown{-webkit-animation-name:bounceInDown;-moz-animation-name:bounceInDown;-o-animation-name:bounceInDown;animation-name:bounceInDown}@-webkit-keyframes bounceOutDown{0%{-webkit-transform:translateY(0)}20%{opacity:1;-webkit-transform:translateY(-20px)}100%{opacity:0;-webkit-transform:translateY(2000px)}}@-moz-keyframes bounceOutDown{0%{-moz-transform:translateY(0)}20%{opacity:1;-moz-transform:translateY(-20px)}100%{opacity:0;-moz-transform:translateY(2000px)}}@keyframes bounceOutDown{0%{transform:translateY(0)}20%{opacity:1;transform:translateY(-20px)}100%{opacity:0;transform:translateY(2000px)}}.bounceOutDown{-webkit-animation-name:bounceOutDown;-moz-animation-name:bounceOutDown;-o-animation-name:bounceOutDown;animation-name:bounceOutDown}',
            s = d.createElement('style');

        var ajaxdata;

        s.type = 'text/css';
        if (s.styleSheet){
            s.styleSheet.cssText = c;
        } else {
            s.appendChild(d.createTextNode(c));
        }

        d.getElementsByTagName('head')[0].appendChild(s);

        t.href = '#';
        t.innerText = 'Loading...';
        l.className = 'rostergenius animated';
        inner.className = 'rostergenius-inner nomouse';
        inner.appendChild(t);
        l.appendChild(inner);
        d.body.appendChild(l);

        var script = d.querySelector('#rostergenius-script');
        var ver = /v=(\w{1,10})&/.exec(script.src)[1];

        setTimeout(function(){
            l.className = 'rostergenius animated bounceInDown';
        }, 10);

        // Check if we're actually on mypage...
        if(location.host.indexOf('mypage.apple') > -1) {
            // We are on mypage
            if(d.querySelectorAll('#kronosSchedule').length > 0) {
                var r = d.getElementsByTagName('table')[2].innerText.replace(/\s+/g, ' ').split('Sun Mon Tue')[0].split(' ');
                r = r.slice(5,r.length-3).toString().replace(/,/g, ' ');

                var roster = d.getElementsByTagName('table')[2].querySelector('tr:first-of-type td:nth-of-type(2)');
                var days = roster.querySelectorAll('table:nth-of-type(2) > tbody >  tr:not(.disable)');
                var sat = roster.querySelector('table:first-of-type td:first-of-type').innerText;
                var rosterToSend = sat;
                var daytext;

                for(var row in days) {
                    daytext = days[row].innerText;
                    if(daytext){
                        rosterToSend += '\n' + daytext.replace(/\s+/g, ' ');
                    }
                }

                if(r.indexOf('begins') > -1) {
                    var xhr = null;
                    xhr = new XMLHttpRequest();
                    xhr.onreadystatechange = function() {
                        if (xhr.readyState === 4 && xhr.status === 200) {
                            window.RGwidgetLoaded(inner, xhr);
                        } else if (xhr.readyState === 4 && xhr.status !== 200) {
                            try {
                                ajaxdata = JSON.parse(xhr.responseText);
                                t.innerText = 'Error: ' + ajaxdata.message;
                            } catch (e) {
                                t.innerText = 'An error occured.';
                            }
                        }
                    };
                    xhr.open( 'POST', protocol + '//rostergeni.us/parse/', true );
                    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
                    xhr.send('bm=1&v='+encodeURIComponent(ver)+'&roster='+encodeURIComponent(rosterToSend));
                } else {
                    t.innerText = 'Could\'nt find your schedule.';
                }
            } else {
                t.innerText = 'You must be on your schedule to use Roster Genius.';
            }
        } else {
            inner.className = 'rostergenius-inner';
            t.innerText = 'You must be on myPage to use Roster Genius.';
            t.href = 'http://mypage.apple.com';
        }
    }
    window.RGmain(document);
})();