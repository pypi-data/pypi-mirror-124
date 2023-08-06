(window.webpackJsonp=window.webpackJsonp||[]).push([[22],{4681:function(e,t,a){"use strict";a.d(t,"a",(function(){return b}));var l=a(11),n=a.n(l),s=(a(0),a(40)),c=a(51),o=a(31),r=a(1);const i=s.g.span`
  white-space: nowrap;
  min-width: 100px;
  svg,
  i {
    margin-right: 8px;

    &:hover {
      path {
        fill: ${({theme:e})=>e.colors.primary.base};
      }
    }
  }
`,d=s.g.span`
  color: ${({theme:e})=>e.colors.grayscale.base};
`;function b({actions:e}){return Object(r.jsx)(i,{className:"actions"},n()(e).call(e,(e,t)=>{const a=o.a[e.icon];return e.tooltip?Object(r.jsx)(c.a,{id:`${e.label}-tooltip`,title:e.tooltip,placement:e.placement,key:t},Object(r.jsx)(d,{role:"button",tabIndex:0,className:"action-button",onClick:e.onClick},Object(r.jsx)(a,null))):Object(r.jsx)(d,{role:"button",tabIndex:0,className:"action-button",onClick:e.onClick,key:t},Object(r.jsx)(a,null))}))}},4727:function(e,t,a){"use strict";var l,n;a.d(t,"a",(function(){return l})),a.d(t,"b",(function(){return n})),function(e){e.success="Success",e.working="Working",e.error="Error",e.noop="Not triggered",e.grace="On Grace"}(l||(l={})),function(e){e.email="Email",e.slack="Slack"}(n||(n={}))},4766:function(e,t,a){"use strict";a.d(t,"a",(function(){return d}));var l=a(40),n=a(13),s=(a(0),a(51)),c=a(31),o=a(4727),r=a(1);function i(e,t,a){switch(e){case o.a.working:return a.colors.primary.base;case o.a.error:return a.colors.error.base;case o.a.success:return t?a.colors.success.base:a.colors.alert.base;case o.a.noop:return a.colors.success.base;case o.a.grace:return a.colors.alert.base;default:return a.colors.grayscale.base}}function d({state:e,isReportEnabled:t=!1}){const a=Object(l.i)(),d={icon:c.a.Check,label:"",status:""};switch(e){case o.a.success:d.icon=t?c.a.Check:c.a.AlertSolidSmall,d.label=t?Object(n.e)("Report sent"):Object(n.e)("Alert triggered, notification sent"),d.status=o.a.success;break;case o.a.working:d.icon=c.a.Running,d.label=t?Object(n.e)("Report sending"):Object(n.e)("Alert running"),d.status=o.a.working;break;case o.a.error:d.icon=c.a.XSmall,d.label=t?Object(n.e)("Report failed"):Object(n.e)("Alert failed"),d.status=o.a.error;break;case o.a.noop:d.icon=c.a.Check,d.label=Object(n.e)("Nothing triggered"),d.status=o.a.noop;break;case o.a.grace:d.icon=c.a.AlertSolidSmall,d.label=Object(n.e)("Alert Triggered, In Grace Period"),d.status=o.a.grace;break;default:d.icon=c.a.Check,d.label=Object(n.e)("Nothing triggered"),d.status=o.a.noop}const b=d.icon;return Object(r.jsx)(s.a,{title:d.label,placement:"bottomLeft"},Object(r.jsx)(b,{iconColor:i(d.status,t,a)}))}},5058:function(e,t,a){"use strict";a.r(t);a(41);var l=a(35),n=a.n(l),s=a(11),c=a.n(s),o=a(0),r=a.n(o),i=a(365),d=a(215),b=a(40),u=a(13),j=a(66),p=a(37),O=a.n(p),h=a(4681),m=a(45),g=a(672),v=a(51),x=a(4669),f=a(720),y=a(1937),_=a(104),N=a(142),w=a(4766),k=a(1),S=a(31),C=a(4727);const $=e=>k.css`
  color: ${e.colors.grayscale.light1};
  margin-right: ${2*e.gridUnit}px;
`;function A({type:e}){const t={icon:null,label:""};switch(e){case C.b.email:t.icon=Object(k.jsx)(S.a.Email,{css:$}),t.label=Object(u.e)(`${C.b.email}`);break;case C.b.slack:t.icon=Object(k.jsx)(S.a.Slack,{css:$}),t.label=Object(u.e)(`${C.b.slack}`);break;default:t.icon=null,t.label=""}return t.icon?Object(k.jsx)(v.a,{title:t.label,placement:"bottom"},t.icon):null}var R=a(1584),q=a(961),E=a(1174),T=a.n(E);O.a.updateLocale("en",{calendar:{lastDay:"[Yesterday at] LTS",sameDay:"[Today at] LTS",nextDay:"[Tomorrow at] LTS",lastWeek:"[last] dddd [at] LTS",nextWeek:"dddd [at] LTS",sameElse:"L"}});const U=b.g.span`
  color: ${({theme:e})=>e.colors.grayscale.base};
`,z=Object(b.g)(S.a.Refresh)`
  color: ${({theme:e})=>e.colors.primary.base};
  width: auto;
  height: ${({theme:e})=>5*e.gridUnit}px;
  position: relative;
  top: ${({theme:e})=>e.gridUnit}px;
  left: ${({theme:e})=>e.gridUnit}px;
  cursor: pointer;
`;var L=({updatedAt:e,update:t})=>{const[a,l]=Object(o.useState)(O()(e));return Object(o.useEffect)(()=>{l(()=>O()(e));const t=T()(()=>{l(()=>O()(e))},6e4);return()=>clearInterval(t)},[e]),Object(k.jsx)(U,null,Object(u.e)("Last Updated %s",a.isValid()?a.calendar():"--"),t&&Object(k.jsx)(z,{onClick:t}))},D=a(418),H=a(117),P=a(32),B=a.n(P),G=a(26),I=a.n(G),V=a(177),M=a.n(V),W=a(36),F=a.n(W),J=a(111),Q=a.n(J),X=a(114),Y=a(1943),K=a(199),Z=a(69),ee=a(42),te=a(1295),ae=a(19),le=a(1944);const ne=({value:e,onChange:t})=>{const a=Object(b.i)(),l=Object(o.useRef)(null),[n,s]=Object(o.useState)("picker"),c=Object(o.useCallback)(e=>{var a;t(e),null==(a=l.current)||a.setValue(e)},[l,t]),[i,d]=Object(o.useState)();return Object(k.jsx)(r.a.Fragment,null,Object(k.jsx)(K.a.Group,{onChange:e=>s(e.target.value),value:n},Object(k.jsx)("div",{className:"inline-container add-margin"},Object(k.jsx)(K.a,{value:"picker"}),Object(k.jsx)(le.CronPicker,{clearButton:!1,value:e,setValue:c,disabled:"picker"!==n,displayError:"picker"===n,onError:d})),Object(k.jsx)("div",{className:"inline-container add-margin"},Object(k.jsx)(K.a,{value:"input"}),Object(k.jsx)("span",{className:"input-label"},"CRON Schedule"),Object(k.jsx)(me,{className:"styled-input"},Object(k.jsx)("div",{className:"input-container"},Object(k.jsx)(ae.m,{type:"text",name:"crontab",ref:l,style:i?{borderColor:a.colors.error.base}:{},placeholder:Object(u.e)("CRON expression"),disabled:"input"!==n,onBlur:e=>{t(e.target.value)},onPressEnter:()=>{var e;t((null==(e=l.current)?void 0:e.input.value)||"")}}))))))},se=b.g.div`
  margin-bottom: 10px;

  .input-container {
    textarea {
      height: auto;
    }
  }

  .inline-container {
    margin-bottom: 10px;

    .input-container {
      margin-left: 10px;
    }

    > div {
      margin: 0;
    }

    .delete-button {
      margin-left: 10px;
      padding-top: 3px;
    }
  }
`,ce=({setting:e=null,index:t,onUpdate:a,onRemove:l})=>{var n;const{method:s,recipients:r,options:i}=e||{},[d,j]=Object(o.useState)(r||""),p=Object(b.i)();if(!e)return null;r&&d!==r&&j(r);const O=c()(n=i||[]).call(n,e=>Object(k.jsx)(Z.d.Option,{key:e,value:e},Object(u.e)(e)));return Object(k.jsx)(se,null,Object(k.jsx)("div",{className:"inline-container"},Object(k.jsx)(me,null,Object(k.jsx)("div",{className:"input-container"},Object(k.jsx)(Z.d,{onChange:l=>{if(j(""),a){const n={...e,method:l,recipients:""};a(t,n)}},placeholder:"Select Delivery Method",defaultValue:s,value:s},O))),void 0!==s&&l?Object(k.jsx)("span",{role:"button",tabIndex:0,className:"delete-button",onClick:()=>l(t)},Object(k.jsx)(S.a.Trash,{iconColor:p.colors.grayscale.base})):null),void 0!==s?Object(k.jsx)(me,null,Object(k.jsx)("div",{className:"control-label"},Object(u.e)(s)),Object(k.jsx)("div",{className:"input-container"},Object(k.jsx)("textarea",{name:"recipients",value:d,onChange:l=>{const{target:n}=l;if(j(n.value),a){const l={...e,recipients:n.value};a(t,l)}}})),Object(k.jsx)("div",{className:"helper"},Object(u.e)('Recipients are separated by "," or ";"'))):null)},oe=["pivot_table","pivot_table_v2","table","paired_ttest"],re=["Email","Slack"],ie=[{label:Object(u.e)("< (Smaller than)"),value:"<"},{label:Object(u.e)("> (Larger than)"),value:">"},{label:Object(u.e)("<= (Smaller or equal)"),value:"<="},{label:Object(u.e)(">= (Larger or equal)"),value:">="},{label:Object(u.e)("== (Is equal)"),value:"=="},{label:Object(u.e)("!= (Is not equal)"),value:"!="},{label:Object(u.e)("Not null"),value:"not null"}],de=[{label:Object(u.e)("None"),value:0},{label:Object(u.e)("30 days"),value:30},{label:Object(u.e)("60 days"),value:60},{label:Object(u.e)("90 days"),value:90}],be={active:!0,creation_method:"alerts_reports",crontab:"0 * * * *",log_retention:90,working_timeout:3600,name:"",owners:[],recipients:[],sql:"",validator_config_json:{},validator_type:"",grace_period:void 0},ue=Object(b.g)(X.b)`
  .ant-modal-body {
    overflow: initial;
  }
`,je=e=>k.css`
  margin: auto ${2*e.gridUnit}px auto 0;
  color: ${e.colors.grayscale.base};
`,pe=b.g.div`
  display: flex;
  min-width: 1000px;
  flex-direction: column;

  .header-section {
    display: flex;
    flex: 0 0 auto;
    align-items: center;
    width: 100%;
    padding: ${({theme:e})=>4*e.gridUnit}px;
    border-bottom: 1px solid ${({theme:e})=>e.colors.grayscale.light2};
  }

  .column-section {
    display: flex;
    flex: 1 1 auto;

    .column {
      flex: 1 1 auto;
      min-width: calc(33.33% - ${({theme:e})=>8*e.gridUnit}px);
      padding: ${({theme:e})=>4*e.gridUnit}px;

      .async-select {
        margin: 10px 0 20px;
      }

      &.condition {
        border-right: 1px solid ${({theme:e})=>e.colors.grayscale.light2};
      }

      &.message {
        border-left: 1px solid ${({theme:e})=>e.colors.grayscale.light2};
      }
    }
  }

  .inline-container {
    display: flex;
    flex-direction: row;
    align-items: center;
    &.wrap {
      flex-wrap: wrap;
    }

    > div {
      flex: 1 1 auto;
    }

    &.add-margin {
      margin-bottom: 5px;
    }

    .styled-input {
      margin: 0 0 0 10px;

      input {
        flex: 0 0 auto;
      }
    }
  }

  .hide-dropdown {
    display: none;
  }
`,Oe=b.g.div`
  display: flex;
  align-items: center;
  margin: ${({theme:e})=>2*e.gridUnit}px auto
    ${({theme:e})=>4*e.gridUnit}px auto;

  h4 {
    margin: 0;
  }

  .required {
    margin-left: ${({theme:e})=>e.gridUnit}px;
    color: ${({theme:e})=>e.colors.error.base};
  }
`,he=b.g.div`
  display: flex;
  align-items: center;
  margin-top: 10px;

  .switch-label {
    margin-left: 10px;
  }
`,me=b.g.div`
  flex: 1 1 auto;
  margin: ${({theme:e})=>2*e.gridUnit}px;
  margin-top: 0;

  .helper {
    display: block;
    color: ${({theme:e})=>e.colors.grayscale.base};
    font-size: ${({theme:e})=>e.typography.sizes.s-1}px;
    padding: ${({theme:e})=>e.gridUnit}px 0;
    text-align: left;
  }

  .required {
    margin-left: ${({theme:e})=>e.gridUnit/2}px;
    color: ${({theme:e})=>e.colors.error.base};
  }

  .input-container {
    display: flex;
    align-items: center;

    > div {
      width: 100%;
    }

    label {
      display: flex;
      margin-right: ${({theme:e})=>2*e.gridUnit}px;
    }

    i {
      margin: 0 ${({theme:e})=>e.gridUnit}px;
    }
  }

  input,
  textarea,
  .Select,
  .ant-select {
    flex: 1 1 auto;
  }

  input[disabled] {
    color: ${({theme:e})=>e.colors.grayscale.base};
  }

  textarea {
    height: 300px;
    resize: none;
  }

  input::placeholder,
  textarea::placeholder,
  .Select__placeholder {
    color: ${({theme:e})=>e.colors.grayscale.light1};
  }

  textarea,
  input[type='text'],
  input[type='number'],
  .Select__control,
  .ant-select-single .ant-select-selector {
    padding: ${({theme:e})=>1.5*e.gridUnit}px
      ${({theme:e})=>2*e.gridUnit}px;
    border-style: none;
    border: 1px solid ${({theme:e})=>e.colors.grayscale.light2};
    border-radius: ${({theme:e})=>e.gridUnit}px;

    .ant-select-selection-placeholder,
    .ant-select-selection-item {
      line-height: 24px;
    }

    &[name='description'] {
      flex: 1 1 auto;
    }
  }

  .Select__control {
    padding: 2px 0;
  }

  .input-label {
    margin-left: 10px;
  }
`,ge=Object(b.g)(K.a)`
  display: block;
  line-height: ${({theme:e})=>7*e.gridUnit}px;
`,ve=Object(b.g)(K.a.Group)`
  margin-left: ${({theme:e})=>5.5*e.gridUnit}px;
`,xe=b.g.div`
  color: ${({theme:e})=>e.colors.primary.dark1};
  cursor: pointer;

  i {
    margin-right: ${({theme:e})=>2*e.gridUnit}px;
  }

  &.disabled {
    color: ${({theme:e})=>e.colors.grayscale.light1};
    cursor: default;
  }
`,fe=({status:e="active",onClick:t})=>{if("hidden"===e)return null;return Object(k.jsx)(xe,{className:e,onClick:()=>{"disabled"!==e&&t()}},Object(k.jsx)("i",{className:"fa fa-plus"})," ","active"===e?Object(u.e)("Add notification method"):Object(u.e)("Add delivery method"))};var ye=Object(N.a)(({addDangerToast:e,onAdd:t,onHide:a,show:l,alert:n=null,isReport:s=!1})=>{var r,i;const[d,b]=Object(o.useState)(!0),[p,O]=Object(o.useState)(),[h,m]=Object(o.useState)(!0),[g,v]=Object(o.useState)("dashboard"),[x,f]=Object(o.useState)("PNG"),[_,N]=Object(o.useState)(!1),[w,C]=Object(o.useState)([]),[$,A]=Object(o.useState)([]),[R,q]=Object(o.useState)([]),[E,T]=Object(o.useState)(""),U=null!==n,z="chart"===g&&(Object(ee.c)(ee.a.ALERTS_ATTACH_REPORTS)||s),[L,H]=Object(o.useState)("active"),[P,G]=Object(o.useState)([]),V=(e,t)=>{const a=F()(P).call(P);a[e]=t,G(a),void 0!==t.method&&"hidden"!==L&&H("active")},W=e=>{const t=F()(P).call(P);M()(t).call(t,e,1),G(t),H("active")},{state:{loading:J,resource:X,error:ae},fetchResource:le,createResource:se,updateResource:xe,clearError:ye}=Object(D.l)("report",Object(u.e)("report"),e),_e=()=>{ye(),m(!0),a(),G([]),O({...be}),H("active")},Ne=e=>{const t=e||(null==p?void 0:p.database);if(!t||t.label)return null;let a;return I()(w).call(w,e=>{e.value!==t.value&&e.value!==t.id||(a=e)}),a},we=e=>{const t=e||(null==p?void 0:p.dashboard);if(!t||t.label)return null;let a;return I()($).call($,e=>{e.value!==t.value&&e.value!==t.id||(a=e)}),a},ke=e=>{const t=e||(null==p?void 0:p.chart);if(!t||t.label)return null;let a;return I()(R).call(R,e=>{e.value!==t.value&&e.value!==t.id||(a=e)}),a},Se=(e,t)=>{O(a=>({...a,[e]:t}))},Ce=e=>{const{target:t}=e;Se(t.name,t.value)},$e=e=>{const{target:t}=e,a=+t.value;Se(t.name,0===a?null:a?Math.max(a,1):a)},Ae=()=>{var e,t,a,l,n,c;p&&null!=(e=p.name)&&e.length&&null!=(t=p.owners)&&t.length&&null!=(a=p.crontab)&&a.length&&void 0!==p.working_timeout&&("dashboard"===g&&p.dashboard||"chart"===g&&p.chart)&&(()=>{if(!P.length)return!1;let e=!1;return I()(P).call(P,t=>{var a;t.method&&null!=(a=t.recipients)&&a.length&&(e=!0)}),e})()?s?b(!1):p.database&&null!=(l=p.sql)&&l.length&&(_||null!=(n=p.validator_config_json)&&n.op)&&(_||void 0!==(null==(c=p.validator_config_json)?void 0:c.threshold))?b(!1):b(!0):b(!0)};Object(o.useEffect)(()=>{if(U&&(null==p||!p.id||(null==n?void 0:n.id)!==p.id||h&&l)){if(n&&null!==n.id&&!J&&!ae){const e=n.id||0;le(e)}}else!U&&(!p||p.id||h&&l)&&(O({...be}),G([]),H("active"))},[n]),Object(o.useEffect)(()=>{if(X){var e,t;const a=c()(e=X.recipients||[]).call(e,e=>{const t="string"==typeof e.recipient_config_json?JSON.parse(e.recipient_config_json):{};return{method:e.type,recipients:t.target||e.recipient_config_json,options:re}});G(a),H(a.length===re.length?"hidden":"active"),v(X.chart?"chart":"dashboard"),f(X.chart&&X.report_format||"PNG");const l="string"==typeof X.validator_config_json?JSON.parse(X.validator_config_json):X.validator_config_json;N("not null"===X.validator_type),X.chart&&T(X.chart.viz_type),O({...X,chart:X.chart?ke(X.chart)||{value:X.chart.id,label:X.chart.slice_name}:void 0,dashboard:X.dashboard?we(X.dashboard)||{value:X.dashboard.id,label:X.dashboard.dashboard_title}:void 0,database:X.database?Ne(X.database)||{value:X.database.id,label:X.database.database_name}:void 0,owners:c()(t=X.owners||[]).call(t,e=>({value:e.id,label:`${e.first_name} ${e.last_name}`})),validator_config_json:"not null"===X.validator_type?{op:"not null"}:l})}},[X]);const Re=p||{};Object(o.useEffect)(()=>{Ae()},[Re.name,Re.owners,Re.database,Re.sql,Re.validator_config_json,Re.crontab,Re.working_timeout,Re.dashboard,Re.chart,g,P,_]),h&&l&&m(!1);const qe=c()(ie).call(ie,e=>Object(k.jsx)(Z.d.Option,{key:e.value,value:e.value},e.label)),Ee=c()(de).call(de,e=>Object(k.jsx)(Z.d.Option,{key:e.value,value:e.value},e.label));return Object(k.jsx)(ue,{className:"no-content-padding",responsive:!0,disablePrimaryButton:d,onHandledPrimaryAction:()=>{var e,a,l,n;const o=[];I()(P).call(P,e=>{e.method&&e.recipients.length&&o.push({recipient_config_json:{target:e.recipients},type:e.method})});const r={...p,type:s?"Report":"Alert",validator_type:_?"not null":"operator",validator_config_json:_?{}:null==p?void 0:p.validator_config_json,chart:"chart"===g?null==p?void 0:null==(e=p.chart)?void 0:e.value:null,dashboard:"dashboard"===g?null==p?void 0:null==(a=p.dashboard)?void 0:a.value:null,database:null==p?void 0:null==(l=p.database)?void 0:l.value,owners:c()(n=(null==p?void 0:p.owners)||[]).call(n,e=>e.value),recipients:o,report_format:"dashboard"===g?"PNG":x||"PNG"};if(r.recipients&&!r.recipients.length&&delete r.recipients,r.context_markdown="string",U){if(p&&p.id){const e=p.id;delete r.id,delete r.created_by,delete r.last_eval_dttm,delete r.last_state,delete r.last_value,delete r.last_value_row_json,xe(e,r).then(e=>{e&&(t&&t(),_e())})}}else p&&se(r).then(e=>{e&&(t&&t(e),_e())})},onHide:_e,primaryButtonName:U?Object(u.e)("Save"):Object(u.e)("Add"),show:l,width:"100%",maxWidth:"1450px",title:Object(k.jsx)("h4",null,U?Object(k.jsx)(S.a.EditAlt,{css:je}):Object(k.jsx)(S.a.PlusLarge,{css:je}),U?Object(u.e)(`Edit ${s?"Report":"Alert"}`):Object(u.e)(`Add ${s?"Report":"Alert"}`))},Object(k.jsx)(pe,null,Object(k.jsx)("div",{className:"header-section"},Object(k.jsx)(me,null,Object(k.jsx)("div",{className:"control-label"},s?Object(u.e)("Report name"):Object(u.e)("Alert name"),Object(k.jsx)("span",{className:"required"},"*")),Object(k.jsx)("div",{className:"input-container"},Object(k.jsx)("input",{type:"text",name:"name",value:p?p.name:"",placeholder:s?Object(u.e)("Report name"):Object(u.e)("Alert name"),onChange:Ce}))),Object(k.jsx)(me,null,Object(k.jsx)("div",{className:"control-label"},Object(u.e)("Owners"),Object(k.jsx)("span",{className:"required"},"*")),Object(k.jsx)("div",{className:"input-container"},Object(k.jsx)(Z.b,{name:"owners",isMulti:!0,value:p?p.owners:[],loadOptions:(e="")=>{const t=Q.a.encode({filter:e,page_size:2e3});return j.a.get({endpoint:`/api/v1/report/related/owners?q=${t}`}).then(e=>{var t;return c()(t=e.json.result).call(t,e=>({value:e.value,label:e.text}))},e=>[])},defaultOptions:!0,cacheOptions:!0,onChange:e=>{Se("owners",e||[])}}))),Object(k.jsx)(me,null,Object(k.jsx)("div",{className:"control-label"},Object(u.e)("Description")),Object(k.jsx)("div",{className:"input-container"},Object(k.jsx)("input",{type:"text",name:"description",value:p&&p.description||"",placeholder:Object(u.e)("Description"),onChange:Ce}))),Object(k.jsx)(he,null,Object(k.jsx)(y.a,{onChange:e=>{Se("active",e)},checked:!p||p.active}),Object(k.jsx)("div",{className:"switch-label"},"Active"))),Object(k.jsx)("div",{className:"column-section"},!s&&Object(k.jsx)("div",{className:"column condition"},Object(k.jsx)(Oe,null,Object(k.jsx)("h4",null,Object(u.e)("Alert condition"))),Object(k.jsx)(me,null,Object(k.jsx)("div",{className:"control-label"},Object(u.e)("Database"),Object(k.jsx)("span",{className:"required"},"*")),Object(k.jsx)("div",{className:"input-container"},Object(k.jsx)(Z.b,{name:"source",value:null!=p&&p.database?{value:p.database.value,label:p.database.label}:void 0,loadOptions:(e="")=>{const t=Q.a.encode({filter:e,page_size:2e3});return j.a.get({endpoint:`/api/v1/report/related/database?q=${t}`}).then(e=>{var t;const a=c()(t=e.json.result).call(t,e=>({value:e.value,label:e.text}));return C(a),p&&p.database&&!p.database.label&&Se("database",Ne()),a},e=>[])},defaultOptions:!0,cacheOptions:!0,onChange:e=>{Se("database",e||[])}}))),Object(k.jsx)(me,null,Object(k.jsx)("div",{className:"control-label"},Object(u.e)("SQL Query"),Object(k.jsx)("span",{className:"required"},"*")),Object(k.jsx)(te.a,{name:"sql",language:"sql",offerEditInModal:!1,minLines:15,maxLines:15,onChange:e=>{Se("sql",e||"")},readOnly:!1,value:p?p.sql:""})),Object(k.jsx)("div",{className:"inline-container wrap"},Object(k.jsx)(me,null,Object(k.jsx)("div",{className:"control-label"},Object(u.e)("Trigger Alert If..."),Object(k.jsx)("span",{className:"required"},"*")),Object(k.jsx)("div",{className:"input-container"},Object(k.jsx)(Z.d,{onChange:e=>{var t;N("not null"===e);const a={op:e,threshold:p?null==(t=p.validator_config_json)?void 0:t.threshold:void 0};Se("validator_config_json",a)},placeholder:"Condition",defaultValue:p&&(null==(r=p.validator_config_json)?void 0:r.op)||void 0,value:p&&(null==(i=p.validator_config_json)?void 0:i.op)||void 0},qe))),Object(k.jsx)(me,null,Object(k.jsx)("div",{className:"control-label"},Object(u.e)("Value"),Object(k.jsx)("span",{className:"required"},"*")),Object(k.jsx)("div",{className:"input-container"},Object(k.jsx)("input",{type:"number",name:"threshold",disabled:_,value:p&&p.validator_config_json&&void 0!==p.validator_config_json.threshold?p.validator_config_json.threshold:"",placeholder:Object(u.e)("Value"),onChange:e=>{var t;const{target:a}=e,l={op:p?null==(t=p.validator_config_json)?void 0:t.op:void 0,threshold:a.value};Se("validator_config_json",l)}}))))),Object(k.jsx)("div",{className:"column schedule"},Object(k.jsx)(Oe,null,Object(k.jsx)("h4",null,s?Object(u.e)("Report schedule"):Object(u.e)("Alert condition schedule")),Object(k.jsx)("span",{className:"required"},"*")),Object(k.jsx)(ne,{value:(null==p?void 0:p.crontab)||"0 * * * *",onChange:e=>Se("crontab",e)}),Object(k.jsx)("div",{className:"control-label"},Object(u.e)("Timezone")),Object(k.jsx)("div",{className:"input-container",css:e=>(e=>k.css`
  margin: ${3*e.gridUnit}px 0;
`)(e)},Object(k.jsx)(Y.a,{onTimezoneChange:e=>{Se("timezone",e)},timezone:null==p?void 0:p.timezone})),Object(k.jsx)(Oe,null,Object(k.jsx)("h4",null,Object(u.e)("Schedule settings"))),Object(k.jsx)(me,null,Object(k.jsx)("div",{className:"control-label"},Object(u.e)("Log retention"),Object(k.jsx)("span",{className:"required"},"*")),Object(k.jsx)("div",{className:"input-container"},Object(k.jsx)(Z.d,{onChange:e=>{Se("log_retention",e)},placeholder:!0,defaultValue:p&&p.log_retention||90,value:p&&p.log_retention||90},Ee))),Object(k.jsx)(me,null,Object(k.jsx)("div",{className:"control-label"},Object(u.e)("Working timeout"),Object(k.jsx)("span",{className:"required"},"*")),Object(k.jsx)("div",{className:"input-container"},Object(k.jsx)("input",{type:"number",min:"1",name:"working_timeout",value:(null==p?void 0:p.working_timeout)||"",placeholder:Object(u.e)("Time in seconds"),onChange:$e}),Object(k.jsx)("span",{className:"input-label"},"seconds"))),!s&&Object(k.jsx)(me,null,Object(k.jsx)("div",{className:"control-label"},Object(u.e)("Grace period")),Object(k.jsx)("div",{className:"input-container"},Object(k.jsx)("input",{type:"number",min:"1",name:"grace_period",value:(null==p?void 0:p.grace_period)||"",placeholder:Object(u.e)("Time in seconds"),onChange:$e}),Object(k.jsx)("span",{className:"input-label"},"seconds")))),Object(k.jsx)("div",{className:"column message"},Object(k.jsx)(Oe,null,Object(k.jsx)("h4",null,Object(u.e)("Message content")),Object(k.jsx)("span",{className:"required"},"*")),Object(k.jsx)(K.a.Group,{onChange:e=>{const{target:t}=e;v(t.value)},value:g},Object(k.jsx)(ge,{value:"dashboard"},Object(u.e)("Dashboard")),Object(k.jsx)(ge,{value:"chart"},Object(u.e)("Chart"))),Object(k.jsx)(Z.b,{className:"chart"===g?"async-select":"hide-dropdown async-select",name:"chart",value:p&&p.chart?{value:p.chart.value,label:p.chart.label}:void 0,loadOptions:(e="")=>{const t=Q.a.encode({filter:e,page_size:2e3});return j.a.get({endpoint:`/api/v1/report/related/chart?q=${t}`}).then(e=>{var t;const a=c()(t=e.json.result).call(t,e=>({value:e.value,label:e.text}));return q(a),p&&p.chart&&!p.chart.label&&Se("chart",ke()),a},e=>[])},defaultOptions:!0,cacheOptions:!0,onChange:e=>{(e=>{j.a.get({endpoint:`/api/v1/chart/${e.value}`}).then(e=>T(e.json.result.viz_type))})(e),Se("chart",e||void 0),Se("dashboard",null)}}),Object(k.jsx)(Z.b,{className:"dashboard"===g?"async-select":"hide-dropdown async-select",name:"dashboard",value:p&&p.dashboard?{value:p.dashboard.value,label:p.dashboard.label}:void 0,loadOptions:(e="")=>{const t=Q.a.encode({filter:e,page_size:2e3});return j.a.get({endpoint:`/api/v1/report/related/dashboard?q=${t}`}).then(e=>{var t;const a=c()(t=e.json.result).call(t,e=>({value:e.value,label:e.text}));return A(a),p&&p.dashboard&&!p.dashboard.label&&Se("dashboard",we()),a},e=>[])},defaultOptions:!0,cacheOptions:!0,onChange:e=>{Se("dashboard",e||void 0),Se("chart",null)}}),z&&Object(k.jsx)("div",{className:"inline-container"},Object(k.jsx)(ve,{onChange:e=>{const{target:t}=e;f(t.value)},value:x},Object(k.jsx)(ge,{value:"PNG"},Object(u.e)("Send as PNG")),Object(k.jsx)(ge,{value:"CSV"},Object(u.e)("Send as CSV")),B()(oe).call(oe,E)&&Object(k.jsx)(ge,{value:"TEXT"},Object(u.e)("Send as text")))),Object(k.jsx)(Oe,null,Object(k.jsx)("h4",null,Object(u.e)("Notification method")),Object(k.jsx)("span",{className:"required"},"*")),c()(P).call(P,(e,t)=>Object(k.jsx)(ce,{setting:e,index:t,onUpdate:V,onRemove:W})),Object(k.jsx)(fe,{status:L,onClick:()=>{const e=F()(P).call(P);e.push({recipients:"",options:re}),G(e),H(e.length===re.length?"hidden":"disabled")}})))))});const _e=Object(d.a)({requestType:"rison",method:"DELETE",endpoint:"/api/v1/report/"}),Ne=b.g.div`
  width: 100%;
  padding: 0 ${({theme:e})=>4*e.gridUnit}px
    ${({theme:e})=>3*e.gridUnit}px;
  background-color: ${({theme:e})=>e.colors.grayscale.light5};
`;t.default=Object(N.a)((function({addDangerToast:e,isReportEnabled:t=!1,user:a,addSuccessToast:l}){const s=t?Object(u.e)("report"):Object(u.e)("alert"),d=t?Object(u.e)("reports"):Object(u.e)("alerts"),b=t?"Reports":"Alerts",p=Object(o.useMemo)(()=>[{id:"type",operator:x.a.equals,value:t?"Report":"Alert"}],[t]),{state:{loading:N,resourceCount:S,resourceCollection:$,bulkSelectEnabled:E,lastFetched:T},hasPerm:U,fetchData:z,refreshData:P,toggleBulkSelect:B}=Object(D.k)("report",Object(u.e)("reports"),e,!0,void 0,p),{updateResource:G}=Object(D.l)("report",Object(u.e)("reports"),e),[I,V]=Object(o.useState)(!1),[M,W]=Object(o.useState)(null),[F,J]=Object(o.useState)(null);function Q(e){W(e),V(!0)}const X=U("can_write"),Y=U("can_write"),K=U("can_write");Object(o.useEffect)(()=>{E&&Y&&B()},[t]);const Z=[{id:"name",desc:!0}],ee=Object(o.useMemo)(()=>[{Cell:({row:{original:{last_state:e}}})=>Object(k.jsx)(w.a,{state:e,isReportEnabled:t}),accessor:"last_state",size:"xs",disableSortBy:!0},{Cell:({row:{original:{last_eval_dttm:e}}})=>e?O.a.utc(e).local().format(_.c):"",accessor:"last_eval_dttm",Header:Object(u.e)("Last run"),size:"lg"},{accessor:"name",Header:Object(u.e)("Name"),size:"xl"},{Header:Object(u.e)("Schedule"),accessor:"crontab_humanized",size:"xl",Cell:({row:{original:{crontab_humanized:e=""}}})=>Object(k.jsx)(v.a,{title:e,placement:"topLeft"},Object(k.jsx)("span",null,e))},{Cell:({row:{original:{recipients:e}}})=>c()(e).call(e,e=>Object(k.jsx)(A,{key:e.id,type:e.type})),accessor:"recipients",Header:Object(u.e)("Notification method"),disableSortBy:!0,size:"xl"},{accessor:"created_by",disableSortBy:!0,hidden:!0,size:"xl"},{Cell:({row:{original:{owners:e=[]}}})=>Object(k.jsx)(g.a,{users:e}),Header:Object(u.e)("Owners"),id:"owners",disableSortBy:!0,size:"xl"},{Cell:({row:{original:e}})=>Object(k.jsx)(y.a,{checked:e.active,onClick:t=>((e,t)=>{if(e&&e.id){const a=e.id;G(a,{active:t}).then(()=>{P()})}})(e,t),size:"small"}),Header:Object(u.e)("Active"),accessor:"active",id:"active",size:"xl"},{Cell:({row:{original:e}})=>{var t;const a=Object(i.f)(),l=n()(t=[X?{label:"execution-log-action",tooltip:Object(u.e)("Execution log"),placement:"bottom",icon:"Note",onClick:()=>a.push(`/${e.type.toLowerCase()}/${e.id}/log`)}:null,X?{label:"edit-action",tooltip:Object(u.e)("Edit"),placement:"bottom",icon:"Edit",onClick:()=>Q(e)}:null,Y?{label:"delete-action",tooltip:Object(u.e)("Delete"),placement:"bottom",icon:"Trash",onClick:()=>J(e)}:null]).call(t,e=>null!==e);return Object(k.jsx)(h.a,{actions:l})},Header:Object(u.e)("Actions"),id:"actions",hidden:!X&&!Y,disableSortBy:!0,size:"xl"}],[Y,X,t]),te=[];K&&te.push({name:Object(k.jsx)(r.a.Fragment,null,Object(k.jsx)("i",{className:"fa fa-plus"})," ",s),buttonStyle:"primary",onClick:()=>{Q(null)}}),Y&&te.push({name:Object(u.e)("Bulk select"),onClick:B,buttonStyle:"secondary","data-test":"bulk-select-toggle"});const ae=Object(k.jsx)(m.a,{buttonStyle:"primary",onClick:()=>Q(null)},Object(k.jsx)("i",{className:"fa fa-plus"})," ",s),le={message:Object(u.e)("No %s yet",d),slot:K?ae:null},ne=Object(o.useMemo)(()=>[{Header:Object(u.e)("Created by"),id:"created_by",input:"select",operator:x.a.relationOneMany,unfilteredLabel:"All",fetchSelects:Object(H.g)("report","created_by",Object(H.e)(e=>Object(u.e)("An error occurred while fetching created by values: %s",e)),a.userId),paginate:!0},{Header:Object(u.e)("Status"),id:"last_state",input:"select",operator:x.a.equals,unfilteredLabel:"Any",selects:[{label:Object(u.e)(`${C.a.success}`),value:C.a.success},{label:Object(u.e)(`${C.a.working}`),value:C.a.working},{label:Object(u.e)(`${C.a.error}`),value:C.a.error},{label:Object(u.e)(`${C.a.noop}`),value:C.a.noop},{label:Object(u.e)(`${C.a.grace}`),value:C.a.grace}]},{Header:Object(u.e)("Search"),id:"name",input:"search",operator:x.a.contains}],[]);return Object(k.jsx)(r.a.Fragment,null,Object(k.jsx)(f.a,{activeChild:b,name:Object(u.e)("Alerts & reports"),tabs:[{name:"Alerts",label:Object(u.e)("Alerts"),url:"/alert/list/",usesRouter:!0,"data-test":"alert-list"},{name:"Reports",label:Object(u.e)("Reports"),url:"/report/list/",usesRouter:!0,"data-test":"report-list"}],buttons:te},Object(k.jsx)(Ne,null,Object(k.jsx)(L,{updatedAt:T,update:()=>P()}))),Object(k.jsx)(ye,{alert:M,addDangerToast:e,layer:M,onHide:()=>{V(!1),W(null),P()},show:I,isReport:t}),F&&Object(k.jsx)(q.a,{description:Object(u.e)("This action will permanently delete %s.",F.name),onConfirm:()=>{F&&(({id:t,name:a})=>{j.a.delete({endpoint:`/api/v1/report/${t}`}).then(()=>{P(),J(null),l(Object(u.e)("Deleted: %s",a))},Object(H.e)(t=>e(Object(u.e)("There was an issue deleting %s: %s",a,t))))})(F)},onHide:()=>J(null),open:!0,title:Object(u.e)("Delete %s?",s)}),Object(k.jsx)(R.a,{title:Object(u.e)("Please confirm"),description:Object(u.e)("Are you sure you want to delete the selected %s?",d),onConfirm:async t=>{try{const{message:e}=await _e(c()(t).call(t,({id:e})=>e));P(),l(e)}catch(t){Object(H.e)(t=>e(Object(u.e)("There was an issue deleting the selected %s: %s",d,t)))(t)}}},e=>{const t=Y?[{key:"delete",name:Object(u.e)("Delete"),onSelect:e,type:"danger"}]:[];return Object(k.jsx)(x.b,{className:"alerts-list-view",columns:ee,count:S,data:$,emptyState:le,fetchData:z,filters:ne,initialSort:Z,loading:N,bulkActions:t,bulkSelectEnabled:E,disableBulkSelect:B,pageSize:25})}))}))}}]);