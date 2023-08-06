(window.webpackJsonp=window.webpackJsonp||[]).push([[30],{4682:function(e,a,t){"use strict";t(41);var n=t(11),s=t.n(n),o=t(35),l=t.n(o),i=t(0),r=t.n(i),c=t(40),d=t(13),p=t(45),b=t(114),u=t(19),h=t(418),m=t(1);const g=c.g.div`
  display: block;
  color: ${({theme:e})=>e.colors.grayscale.base};
  font-size: ${({theme:e})=>e.typography.sizes.s-1}px;
`,j=c.g.div`
  padding-bottom: ${({theme:e})=>2*e.gridUnit}px;
  padding-top: ${({theme:e})=>2*e.gridUnit}px;

  & > div {
    margin: ${({theme:e})=>e.gridUnit}px 0;
  }

  &.extra-container {
    padding-top: 8px;
  }

  .confirm-overwrite {
    margin-bottom: ${({theme:e})=>2*e.gridUnit}px;
  }

  .input-container {
    display: flex;
    align-items: center;

    label {
      display: flex;
      margin-right: ${({theme:e})=>2*e.gridUnit}px;
    }

    i {
      margin: 0 ${({theme:e})=>e.gridUnit}px;
    }
  }

  input,
  textarea {
    flex: 1 1 auto;
  }

  textarea {
    height: 160px;
    resize: none;
  }

  input::placeholder,
  textarea::placeholder {
    color: ${({theme:e})=>e.colors.grayscale.light1};
  }

  textarea,
  input[type='text'],
  input[type='number'] {
    padding: ${({theme:e})=>1.5*e.gridUnit}px
      ${({theme:e})=>2*e.gridUnit}px;
    border-style: none;
    border: 1px solid ${({theme:e})=>e.colors.grayscale.light2};
    border-radius: ${({theme:e})=>e.gridUnit}px;

    &[name='name'] {
      flex: 0 1 auto;
      width: 40%;
    }

    &[name='sqlalchemy_uri'] {
      margin-right: ${({theme:e})=>3*e.gridUnit}px;
    }
  }
`;a.a=({resourceName:e,resourceLabel:a,passwordsNeededMessage:t,confirmOverwriteMessage:n,addDangerToast:o,addSuccessToast:c,onModelImport:x,show:O,onHide:v,passwordFields:y=[],setPasswordFields:f=(()=>{})})=>{const[_,C]=Object(i.useState)(!0),[w,$]=Object(i.useState)({}),[N,E]=Object(i.useState)(!1),[S,k]=Object(i.useState)(!1),[T,A]=Object(i.useState)([]),[U,L]=Object(i.useState)(!1),M=()=>{A([]),f([]),$({}),E(!1),k(!1),L(!1)},{state:{alreadyExists:q,passwordsNeeded:R},importResource:D}=Object(h.j)(e,a,e=>{M(),o(e)});Object(i.useEffect)(()=>{f(R),R.length>0&&L(!1)},[R,f]),Object(i.useEffect)(()=>{E(q.length>0),q.length>0&&L(!1)},[q,E]);const I=e=>{var a,t;const n=null!=(a=null==(t=e.currentTarget)?void 0:t.value)?a:"";k(n.toUpperCase()===Object(d.e)("OVERWRITE"))};return _&&O&&C(!1),Object(m.jsx)(b.b,{name:"model",className:"import-model-modal",disablePrimaryButton:0===T.length||N&&!S||U,onHandledPrimaryAction:()=>{var e;(null==(e=T[0])?void 0:e.originFileObj)instanceof File&&(L(!0),D(T[0].originFileObj,w,S).then(e=>{e&&(c(Object(d.e)("The import was successful")),M(),x())}))},onHide:()=>{C(!0),v(),M()},primaryButtonName:N?Object(d.e)("Overwrite"):Object(d.e)("Import"),primaryButtonType:N?"danger":"primary",width:"750px",show:O,title:Object(m.jsx)("h4",null,Object(d.e)("Import %s",a))},Object(m.jsx)(j,null,Object(m.jsx)(u.F,{name:"modelFile",id:"modelFile",accept:".yaml,.json,.yml,.zip",fileList:T,onChange:e=>{A([{...e.file,status:"done"}])},onRemove:e=>(A(l()(T).call(T,a=>a.uid!==e.uid)),!1),customRequest:()=>{}},Object(m.jsx)(p.a,{loading:U},"Select file"))),0===y.length?null:Object(m.jsx)(r.a.Fragment,null,Object(m.jsx)("h5",null,"Database passwords"),Object(m.jsx)(g,null,t),s()(y).call(y,e=>Object(m.jsx)(j,{key:`password-for-${e}`},Object(m.jsx)("div",{className:"control-label"},e,Object(m.jsx)("span",{className:"required"},"*")),Object(m.jsx)("input",{name:`password-${e}`,autoComplete:`password-${e}`,type:"password",value:w[e],onChange:a=>$({...w,[e]:a.target.value})})))),N?Object(m.jsx)(r.a.Fragment,null,Object(m.jsx)(j,null,Object(m.jsx)("div",{className:"confirm-overwrite"},n),Object(m.jsx)("div",{className:"control-label"},Object(d.e)('Type "%s" to confirm',Object(d.e)("OVERWRITE"))),Object(m.jsx)("input",{id:"overwrite",type:"text",onChange:I}))):null)}},4697:function(e,a,t){"use strict";t.d(a,"a",(function(){return s}));var n=t(13);const s={name:Object(n.e)("Data"),tabs:[{name:"Databases",label:Object(n.e)("Databases"),url:"/databaseview/list/",usesRouter:!0},{name:"Datasets",label:Object(n.e)("Datasets"),url:"/tablemodelview/list/",usesRouter:!0},{name:"Saved queries",label:Object(n.e)("Saved queries"),url:"/savedqueryview/list/",usesRouter:!0},{name:"Query history",label:Object(n.e)("Query history"),url:"/superset/sqllab/history/",usesRouter:!0}]}},5049:function(e,a,t){"use strict";t.r(a);t(41);var n=t(13),s=t(40),o=t(66),l=t(0),i=t.n(l),r=t(171),c=t(42),d=t(418),p=t(117),b=t(142),u=t(720),h=t(961),m=t(51),g=t(31),j=t(4669),x=t(4697),O=t(4682),v=t(1585),y=t(71),f=t.n(y),_=t(26),C=t.n(_),w=t(161),$=t.n(w),N=t(115),E=t.n(N),S=t(54),k=t.n(S),T=t(35),A=t.n(T),U=t(39),L=t.n(U),M=t(86),q=t.n(M),R=t(64),D=t.n(R),I=t(1153),P=t.n(I),z=t(530),F=t.n(z),H=t(177),B=t.n(H),Q=t(11),V=t.n(Q),Y=t(158),J=t.n(Y),W=t(155),G=t(169),X=t(19),K=t(213),Z=t(114),ee=t(45);function ae(){return(ae=Object.assign||function(e){for(var a=1;a<arguments.length;a++){var t=arguments[a];for(var n in t)Object.prototype.hasOwnProperty.call(t,n)&&(e[n]=t[n])}return e}).apply(this,arguments)}const te={position:"absolute",bottom:0,left:0,height:0,overflow:"hidden","padding-top":0,"padding-bottom":0,border:"none"},ne=["box-sizing","width","font-size","font-weight","font-family","font-style","letter-spacing","text-indent","white-space","word-break","overflow-wrap","padding-left","padding-right"];function se(e,a){for(;e&&a--;)e=e.previousElementSibling;return e}const oe={basedOn:void 0,className:"",component:"div",ellipsis:"…",maxLine:1,onReflow(){},text:"",trimRight:!0,winWidth:void 0},le=Object.keys(oe);class ie extends i.a.Component{constructor(e){super(e),this.state={text:e.text,clamped:!1},this.units=[],this.maxLine=0,this.canvas=null}componentDidMount(){this.initCanvas(),this.reflow(this.props)}componentDidUpdate(e){e.winWidth!==this.props.winWidth&&this.copyStyleToCanvas(),this.props!==e&&this.reflow(this.props)}componentWillUnmount(){this.canvas.parentNode.removeChild(this.canvas)}setState(e,a){return void 0!==e.clamped&&(this.clamped=e.clamped),super.setState(e,a)}initCanvas(){if(this.canvas)return;const e=this.canvas=document.createElement("div");e.className=`LinesEllipsis-canvas ${this.props.className}`,e.setAttribute("aria-hidden","true"),this.copyStyleToCanvas(),Object.keys(te).forEach(a=>{e.style[a]=te[a]}),document.body.appendChild(e)}copyStyleToCanvas(){const e=window.getComputedStyle(this.target);ne.forEach(a=>{this.canvas.style[a]=e[a]})}reflow(e){const a=e.basedOn||(/^[\x00-\x7F]+$/.test(e.text)?"words":"letters");switch(a){case"words":this.units=e.text.split(/\b|(?=\W)/);break;case"letters":this.units=Array.from(e.text);break;default:throw new Error(`Unsupported options basedOn: ${a}`)}this.maxLine=+e.maxLine||1,this.canvas.innerHTML=this.units.map(e=>`<span class='LinesEllipsis-unit'>${e}</span>`).join("");const t=this.putEllipsis(this.calcIndexes()),n=t>-1,s={clamped:n,text:n?this.units.slice(0,t).join(""):e.text};this.setState(s,e.onReflow.bind(this,s))}calcIndexes(){const e=[0];let a=this.canvas.firstElementChild;if(!a)return e;let t=0,n=1,s=a.offsetTop;for(;(a=a.nextElementSibling)&&(a.offsetTop>s&&(n++,e.push(t),s=a.offsetTop),t++,!(n>this.maxLine)););return e}putEllipsis(e){if(e.length<=this.maxLine)return-1;const a=e[this.maxLine],t=this.units.slice(0,a),n=this.canvas.children[a].offsetTop;this.canvas.innerHTML=t.map((e,a)=>`<span class='LinesEllipsis-unit'>${e}</span>`).join("")+`<wbr><span class='LinesEllipsis-ellipsis'>${this.props.ellipsis}</span>`;const s=this.canvas.lastElementChild;let o=se(s,2);for(;o&&(s.offsetTop>n||s.offsetHeight>o.offsetHeight||s.offsetTop>o.offsetTop);)this.canvas.removeChild(o),o=se(s,2),t.pop();return t.length}isClamped(){return this.clamped}render(){const{text:e,clamped:a}=this.state,t=this.props,{component:n,ellipsis:s,trimRight:o,className:l}=t,r=function(e,a){if(null==e)return{};var t,n,s={},o=Object.keys(e);for(n=0;n<o.length;n++)t=o[n],a.indexOf(t)>=0||(s[t]=e[t]);return s}(t,["component","ellipsis","trimRight","className"]);return i.a.createElement(n,ae({className:`LinesEllipsis ${a?"LinesEllipsis--clamped":""} ${l}`,ref:e=>this.target=e},function(e,a){if(!e||"object"!=typeof e)return e;const t={};return Object.keys(e).forEach(n=>{a.indexOf(n)>-1||(t[n]=e[n])}),t}(r,le)),a&&o?e.replace(/[\s\uFEFF\xA0]+$/,""):e,i.a.createElement("wbr",null),a&&i.a.createElement("span",{className:"LinesEllipsis-ellipsis"},s))}}ie.defaultProps=oe;var re=ie,ce=t(1);const de=Object(s.g)(ee.a)`
  height: auto;
  display: flex;
  flex-direction: column;
  padding: 0;
`,pe=s.g.div`
  padding: ${({theme:e})=>4*e.gridUnit}px;
  height: ${({theme:e})=>18*e.gridUnit}px;
  margin: ${({theme:e})=>3*e.gridUnit}px 0;

  .default-db-icon {
    font-size: 36px;
    color: ${({theme:e})=>e.colors.grayscale.base};
    margin-right: 0;
    span:first-of-type {
      margin-right: 0;
    }
  }

  &:first-of-type {
    margin-right: 0;
  }

  img {
    width: ${({theme:e})=>10*e.gridUnit}px;
    height: ${({theme:e})=>10*e.gridUnit}px;
    margin: 0;
    &:first-of-type {
      margin-right: 0;
    }
  }
  svg {
    &:first-of-type {
      margin-right: 0;
    }
  }
`,be=s.g.div`
  max-height: calc(1.5em * 2);
  white-space: break-spaces;

  &:first-of-type {
    margin-right: 0;
  }

  .LinesEllipsis {
    &:first-of-type {
      margin-right: 0;
    }
  }
`,ue=s.g.div`
  padding: ${({theme:e})=>4*e.gridUnit}px 0;
  border-radius: 0 0 ${({theme:e})=>e.borderRadius}px
    ${({theme:e})=>e.borderRadius}px;
  background-color: ${({theme:e})=>e.colors.grayscale.light4};
  width: 100%;
  line-height: 1.5em;
  overflow: hidden;
  white-space: no-wrap;
  text-overflow: ellipsis;

  &:first-of-type {
    margin-right: 0;
  }
`;var he,me=Object(s.g)(({icon:e,altText:a,buttonText:t,...n})=>Object(ce.jsx)(de,n,Object(ce.jsx)(pe,null,e&&Object(ce.jsx)("img",{src:e,alt:a}),!e&&Object(ce.jsx)(g.a.DatabaseOutlined,{className:"default-db-icon","aria-label":"default-icon"})),Object(ce.jsx)(ue,null,Object(ce.jsx)(be,null,Object(ce.jsx)(re,{text:t,maxLine:"2",basedOn:"words",trimRight:!0})))))`
  text-transform: none;
  background-color: ${({theme:e})=>e.colors.grayscale.light5};
  font-weight: ${({theme:e})=>e.typography.weights.normal};
  color: ${({theme:e})=>e.colors.grayscale.dark2};
  border: 1px solid ${({theme:e})=>e.colors.grayscale.light2};
  margin: 0;
  width: 100%;

  &:hover,
  &:focus {
    background-color: ${({theme:e})=>e.colors.grayscale.light5};
    color: ${({theme:e})=>e.colors.grayscale.dark2};
    border: 1px solid ${({theme:e})=>e.colors.grayscale.light2};
    box-shadow: 4px 4px 20px ${({theme:e})=>e.colors.grayscale.light2};
  }
`,ge=t(591),je=t(91);!function(e){e.SQLALCHEMY_URI="sqlalchemy_form",e.DYNAMIC_FORM="dynamic_form"}(he||(he={}));var xe=t(5),Oe=t.n(xe),ve=t(4822),ye=t(146),fe=t(310);const _e=ce.css`
  margin-bottom: 0;
`,Ce=s.g.header`
  border-bottom: ${({theme:e})=>`${.25*e.gridUnit}px solid\n    ${e.colors.grayscale.light2};`}
  padding: ${({theme:e})=>2*e.gridUnit}px
    ${({theme:e})=>4*e.gridUnit}px;
  line-height: ${({theme:e})=>6*e.gridUnit}px;

  .helper-top {
    padding-bottom: 0;
    color: ${({theme:e})=>e.colors.grayscale.base};
    font-size: ${({theme:e})=>e.typography.sizes.s-1}px;
    margin: 0;
  }

  .helper-bottom {
    padding-top: 0;
    color: ${({theme:e})=>e.colors.grayscale.base};
    font-size: ${({theme:e})=>e.typography.sizes.s-1}px;
    margin: 0;
  }

  h4 {
    color: ${({theme:e})=>e.colors.grayscale.dark2};
    font-weight: bold;
    font-size: ${({theme:e})=>e.typography.sizes.l}px;
    margin: 0;
    padding: 0;
    line-height: ${({theme:e})=>8*e.gridUnit}px;
  }

  .select-db {
    padding-bottom: ${({theme:e})=>2*e.gridUnit}px;
    .helper {
      margin: 0;
    }

    h4 {
      margin: 0 0 ${({theme:e})=>4*e.gridUnit}px;
    }
  }
`,we=ce.css`
  .ant-tabs-top {
    margin-top: 0;
  }
  .ant-tabs-top > .ant-tabs-nav {
    margin-bottom: 0;
  }
  .ant-tabs-tab {
    margin-right: 0;
  }
`,$e=ce.css`
  .ant-modal-body {
    padding-left: 0;
    padding-right: 0;
    padding-top: 0;
  }
`,Ne=e=>ce.css`
  margin-bottom: ${5*e.gridUnit}px;
  svg {
    margin-bottom: ${.25*e.gridUnit}px;
  }
`,Ee=e=>ce.css`
  padding-left: ${2*e.gridUnit}px;
`,Se=e=>ce.css`
  padding: ${4*e.gridUnit}px ${4*e.gridUnit}px 0;
`,ke=e=>ce.css`
  .ant-select-dropdown {
    height: ${40*e.gridUnit}px;
  }

  .ant-modal-header {
    padding: ${4.5*e.gridUnit}px ${4*e.gridUnit}px
      ${4*e.gridUnit}px;
  }

  .ant-modal-close-x .close {
    color: ${e.colors.grayscale.dark1};
    opacity: 1;
  }

  .ant-modal-title > h4 {
    font-weight: bold;
  }

  .ant-modal-body {
    height: ${180.5*e.gridUnit}px;
  }

  .ant-modal-footer {
    height: ${16.25*e.gridUnit}px;
  }
`,Te=e=>ce.css`
  border: 1px solid ${e.colors.info.base};
  padding: ${4*e.gridUnit}px;
  margin: ${4*e.gridUnit}px 0;

  .ant-alert-message {
    color: ${e.colors.info.dark2};
    font-size: ${e.typography.sizes.s+1}px;
    font-weight: bold;
  }

  .ant-alert-description {
    color: ${e.colors.info.dark2};
    font-size: ${e.typography.sizes.s+1}px;
    line-height: ${4*e.gridUnit}px;

    a {
      text-decoration: underline;
    }

    .ant-alert-icon {
      margin-right: ${2.5*e.gridUnit}px;
      font-size: ${e.typography.sizes.l+1}px;
      position: relative;
      top: ${e.gridUnit/4}px;
    }
  }
`,Ae=s.g.div`
  margin: 0 ${({theme:e})=>4*e.gridUnit}px -${({theme:e})=>4*e.gridUnit}px;
`,Ue=e=>ce.css`
  border: ${e.colors.error.base} 1px solid;
  padding: ${4*e.gridUnit}px;
  margin: ${8*e.gridUnit}px ${4*e.gridUnit}px;
  color: ${e.colors.error.dark2};
  .ant-alert-message {
    font-size: ${e.typography.sizes.s+1}px;
    font-weight: bold;
  }
  .ant-alert-description {
    font-size: ${e.typography.sizes.s+1}px;
    line-height: ${4*e.gridUnit}px;
    .ant-alert-icon {
      margin-right: ${2.5*e.gridUnit}px;
      font-size: ${e.typography.sizes.l+1}px;
      position: relative;
      top: ${e.gridUnit/4}px;
    }
  }
`,Le=e=>ce.css`
  .required {
    margin-left: ${e.gridUnit/2}px;
    color: ${e.colors.error.base};
  }

  .helper {
    display: block;
    padding: ${e.gridUnit}px 0;
    color: ${e.colors.grayscale.light1};
    font-size: ${e.typography.sizes.s-1}px;
    text-align: left;
  }
`,Me=e=>ce.css`
  .form-group {
    margin-bottom: ${4*e.gridUnit}px;
    &-w-50 {
      display: inline-block;
      width: ${`calc(50% - ${4*e.gridUnit}px)`};
      & + .form-group-w-50 {
        margin-left: ${8*e.gridUnit}px;
        margin-bottom: ${10*e.gridUnit}px;
      }
    }
  }
  .control-label {
    color: ${e.colors.grayscale.dark1};
    font-size: ${e.typography.sizes.s-1}px;
  }
  .helper {
    color: ${e.colors.grayscale.light1};
    font-size: ${e.typography.sizes.s-1}px;
    margin-top: ${1.5*e.gridUnit}px;
  }
  .ant-tabs-content-holder {
    overflow: auto;
    max-height: 475px;
  }
`,qe=e=>ce.css`
  label {
    color: ${e.colors.grayscale.dark1};
    font-size: ${e.typography.sizes.s-1}px;
    margin-bottom: 0;
  }
`,Re=s.g.div`
  margin-bottom: ${({theme:e})=>6*e.gridUnit}px;
  &.mb-0 {
    margin-bottom: 0;
  }
  &.mb-8 {
    margin-bottom: ${({theme:e})=>2*e.gridUnit}px;
  }

  .control-label {
    color: ${({theme:e})=>e.colors.grayscale.dark1};
    font-size: ${({theme:e})=>e.typography.sizes.s-1}px;
    margin-bottom: ${({theme:e})=>2*e.gridUnit}px;
  }

  &.extra-container {
    padding-top: 8px;
  }

  .input-container {
    display: flex;
    align-items: top;

    label {
      display: flex;
      margin-left: ${({theme:e})=>2*e.gridUnit}px;
      margin-top: ${({theme:e})=>.75*e.gridUnit}px;
      font-family: ${({theme:e})=>e.typography.families.sansSerif};
      font-size: ${({theme:e})=>e.typography.sizes.m}px;
    }

    i {
      margin: 0 ${({theme:e})=>e.gridUnit}px;
    }
  }

  input,
  textarea {
    flex: 1 1 auto;
  }

  textarea {
    height: 160px;
    resize: none;
  }

  input::placeholder,
  textarea::placeholder {
    color: ${({theme:e})=>e.colors.grayscale.light1};
  }

  textarea,
  input[type='text'],
  input[type='number'] {
    padding: ${({theme:e})=>1.5*e.gridUnit}px
      ${({theme:e})=>2*e.gridUnit}px;
    border-style: none;
    border: 1px solid ${({theme:e})=>e.colors.grayscale.light2};
    border-radius: ${({theme:e})=>e.gridUnit}px;

    &[name='name'] {
      flex: 0 1 auto;
      width: 40%;
    }
  }
  &.expandable {
    height: 0;
    overflow: hidden;
    transition: height 0.25s;
    margin-left: ${({theme:e})=>8*e.gridUnit}px;
    margin-bottom: 0;
    padding: 0;
    .control-label {
      margin-bottom: 0;
    }
    &.open {
      height: ${102}px;
      padding-right: ${({theme:e})=>5*e.gridUnit}px;
    }
  }
`,De=Object(s.g)(fe.d)`
  flex: 1 1 auto;
  border: 1px solid ${({theme:e})=>e.colors.grayscale.light2};
  border-radius: ${({theme:e})=>e.gridUnit}px;
`,Ie=s.g.div`
  padding-top: ${({theme:e})=>e.gridUnit}px;
  .input-container {
    padding-top: ${({theme:e})=>e.gridUnit}px;
    padding-bottom: ${({theme:e})=>e.gridUnit}px;
  }
  &.expandable {
    height: 0;
    overflow: hidden;
    transition: height 0.25s;
    margin-left: ${({theme:e})=>7*e.gridUnit}px;
    &.open {
      height: ${255}px;
      &.ctas-open {
        height: ${357}px;
      }
    }
  }
`,Pe=s.g.div`
  padding: 0 ${({theme:e})=>4*e.gridUnit}px;
  margin-top: ${({theme:e})=>6*e.gridUnit}px;
`,ze=e=>ce.css`
  font-weight: 400;
  text-transform: initial;
  padding-right: ${2*e.gridUnit}px;
`,Fe=s.g.div`
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: 0px;

  .helper {
    color: ${({theme:e})=>e.colors.grayscale.base};
    font-size: ${({theme:e})=>e.typography.sizes.s-1}px;
    margin: 0px;
  }
`,He=(s.g.div`
  color: ${({theme:e})=>e.colors.grayscale.dark2};
  font-weight: bold;
  font-size: ${({theme:e})=>e.typography.sizes.m}px;
`,s.g.div`
  color: ${({theme:e})=>e.colors.grayscale.dark1};
  font-size: ${({theme:e})=>e.typography.sizes.s}px;
`,s.g.div`
  color: ${({theme:e})=>e.colors.grayscale.light1};
  font-size: ${({theme:e})=>e.typography.sizes.s-1}px;
  text-transform: uppercase;
`),Be=s.g.div`
  color: ${({theme:e})=>e.colors.grayscale.dark1};
  font-size: ${({theme:e})=>e.typography.sizes.l}px;
  font-weight: bold;
`,Qe=s.g.div`
  .label-select {
    text-transform: uppercase;
    color: ${({theme:e})=>e.colors.grayscale.dark1};
    font-size: 11px;
    margin: 0 5px ${({theme:e})=>2*e.gridUnit}px;
  }

  .label-paste {
    color: ${({theme:e})=>e.colors.grayscale.light1};
    font-size: 11px;
    line-height: 16px;
  }

  .input-container {
    margin: ${({theme:e})=>7*e.gridUnit}px 0;
    display: flex;
    flex-direction: column;
}
  }
  .input-form {
    height: 100px;
    width: 100%;
    border: 1px solid ${({theme:e})=>e.colors.grayscale.light2};
    border-radius: ${({theme:e})=>e.gridUnit}px;
    resize: vertical;
    padding: ${({theme:e})=>1.5*e.gridUnit}px
      ${({theme:e})=>2*e.gridUnit}px;
    &::placeholder {
      color: ${({theme:e})=>e.colors.grayscale.light1};
    }
  }

  .input-container {
    .input-upload {
      display: none;
    }
    .input-upload-current {
      display: flex;
      justify-content: space-between;
    }
    .input-upload-btn {
      width: ${({theme:e})=>32*e.gridUnit}px
    }
  }`,Ve=s.g.div`
  .preferred {
    .superset-button {
      margin-left: 0;
    }
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
    margin: ${({theme:e})=>4*e.gridUnit}px;
  }

  .preferred-item {
    width: 32%;
    margin-bottom: ${({theme:e})=>2.5*e.gridUnit}px;
  }

  .available {
    margin: ${({theme:e})=>4*e.gridUnit}px;
    .available-label {
      font-size: ${({theme:e})=>1.1*e.typography.sizes.l}px;
      font-weight: bold;
      margin: ${({theme:e})=>6*e.gridUnit}px 0;
    }
    .available-select {
      width: 100%;
    }
  }

  .label-available-select {
    text-transform: uppercase;
    font-size: ${({theme:e})=>e.typography.sizes.s-1}px;
  }

  .control-label {
    color: ${({theme:e})=>e.colors.grayscale.dark1};
    font-size: ${({theme:e})=>e.typography.sizes.s-1}px;
    margin-bottom: ${({theme:e})=>2*e.gridUnit}px;
  }
`,Ye=Object(s.g)(ee.a)`
  width: ${({theme:e})=>40*e.gridUnit}px;
`,Je=s.g.div`
  position: sticky;
  top: 0;
  z-index: ${({theme:e})=>e.zIndex.max};
  background: ${({theme:e})=>e.colors.grayscale.light5};
`,We=s.g.div`
  margin-bottom: 16px;

  .catalog-type-select {
    margin: 0 0 40px;
  }

  .gsheet-title {
    font-size: ${({theme:e})=>1.1*e.typography.sizes.l}px;
    font-weight: bold;
    margin: ${({theme:e})=>6*e.gridUnit}px 0 16px;
  }

  .catalog-label {
    margin: 0 0 8px;
  }

  .catalog-name {
    display: flex;
    .catalog-name-input {
      width: 95%;
    }
  }

  .catalog-name-url {
    margin: 4px 0;
    width: 95%;
  }

  .catalog-delete {
    align-self: center;
    background: ${({theme:e})=>e.colors.grayscale.light4};
    margin: 5px;
  }

  .catalog-add-btn {
    width: 95%;
  }
`;var Ge=({db:e,onInputChange:a,onTextChange:t,onEditorChange:s,onExtraInputChange:o,onExtraEditorChange:l})=>{var i,r,c,d,p,b,u,h,m,g,j;const x=!(null==e||!e.expose_in_sqllab),O=!!(null!=e&&e.allow_ctas||null!=e&&e.allow_cvas);return Object(ce.jsx)(ye.a,{expandIconPosition:"right",accordion:!0,css:e=>(e=>ce.css`
  .ant-collapse-header {
    padding-top: ${3.5*e.gridUnit}px;
    padding-bottom: ${2.5*e.gridUnit}px;

    .anticon.ant-collapse-arrow {
      top: calc(50% - ${6}px);
    }
    .helper {
      color: ${e.colors.grayscale.base};
    }
  }
  h4 {
    font-size: 16px;
    font-weight: bold;
    margin-top: 0;
    margin-bottom: ${e.gridUnit}px;
  }
  p.helper {
    margin-bottom: 0;
    padding: 0;
  }
`)(e)},Object(ce.jsx)(ye.a.Panel,{header:Object(ce.jsx)("div",null,Object(ce.jsx)("h4",null,"SQL Lab"),Object(ce.jsx)("p",{className:"helper"},"Adjust how this database will interact with SQL Lab.")),key:"1"},Object(ce.jsx)(Re,{css:_e},Object(ce.jsx)("div",{className:"input-container"},Object(ce.jsx)(ve.a,{id:"expose_in_sqllab",indeterminate:!1,checked:!(null==e||!e.expose_in_sqllab),onChange:a,labelText:Object(n.e)("Expose database in SQL Lab")}),Object(ce.jsx)(ge.a,{tooltip:Object(n.e)("Allow this database to be queried in SQL Lab")})),Object(ce.jsx)(Ie,{className:Oe()("expandable",{open:x,"ctas-open":O})},Object(ce.jsx)(Re,{css:_e},Object(ce.jsx)("div",{className:"input-container"},Object(ce.jsx)(ve.a,{id:"allow_ctas",indeterminate:!1,checked:!(null==e||!e.allow_ctas),onChange:a,labelText:Object(n.e)("Allow CREATE TABLE AS")}),Object(ce.jsx)(ge.a,{tooltip:Object(n.e)("Allow creation of new tables based on queries")}))),Object(ce.jsx)(Re,{css:_e},Object(ce.jsx)("div",{className:"input-container"},Object(ce.jsx)(ve.a,{id:"allow_cvas",indeterminate:!1,checked:!(null==e||!e.allow_cvas),onChange:a,labelText:Object(n.e)("Allow CREATE VIEW AS")}),Object(ce.jsx)(ge.a,{tooltip:Object(n.e)("Allow creation of new views based on queries")})),Object(ce.jsx)(Re,{className:Oe()("expandable",{open:O})},Object(ce.jsx)("div",{className:"control-label"},Object(n.e)("CTAS & CVAS SCHEMA")),Object(ce.jsx)("div",{className:"input-container"},Object(ce.jsx)("input",{type:"text",name:"force_ctas_schema",value:(null==e?void 0:e.force_ctas_schema)||"",placeholder:Object(n.e)("Create or select schema..."),onChange:a})),Object(ce.jsx)("div",{className:"helper"},Object(n.e)("Force all tables and views to be created in this schema when clicking CTAS or CVAS in SQL Lab.")))),Object(ce.jsx)(Re,{css:_e},Object(ce.jsx)("div",{className:"input-container"},Object(ce.jsx)(ve.a,{id:"allow_dml",indeterminate:!1,checked:!(null==e||!e.allow_dml),onChange:a,labelText:Object(n.e)("Allow DML")}),Object(ce.jsx)(ge.a,{tooltip:Object(n.e)("Allow manipulation of the database using non-SELECT statements such as UPDATE, DELETE, CREATE, etc.")}))),Object(ce.jsx)(Re,{css:_e},Object(ce.jsx)("div",{className:"input-container"},Object(ce.jsx)(ve.a,{id:"allow_multi_schema_metadata_fetch",indeterminate:!1,checked:!(null==e||!e.allow_multi_schema_metadata_fetch),onChange:a,labelText:Object(n.e)("Allow Multi Schema Metadata Fetch")}),Object(ce.jsx)(ge.a,{tooltip:Object(n.e)("Allow SQL Lab to fetch a list of all tables and all views across all database schemas. For large data warehouse with thousands of tables, this can be expensive and put strain on the system.")}))),Object(ce.jsx)(Re,{css:_e},Object(ce.jsx)("div",{className:"input-container"},Object(ce.jsx)(ve.a,{id:"cost_estimate_enabled",indeterminate:!1,checked:!(null==e||null==(i=e.extra_json)||!i.cost_estimate_enabled),onChange:o,labelText:Object(n.e)("Enable query cost estimation")}),Object(ce.jsx)(ge.a,{tooltip:Object(n.e)("For Presto and Postgres, shows a button to compute cost before running a query.")}))),Object(ce.jsx)(Re,null,Object(ce.jsx)("div",{className:"input-container"},Object(ce.jsx)(ve.a,{id:"allows_virtual_table_explore",indeterminate:!1,checked:!(null==e||null==(r=e.extra_json)||!r.allows_virtual_table_explore),onChange:o,labelText:Object(n.e)("Allow this database to be explored")}),Object(ce.jsx)(ge.a,{tooltip:Object(n.e)("When enabled, users are able to visualize SQL Lab results in Explore.")})))))),Object(ce.jsx)(ye.a.Panel,{header:Object(ce.jsx)("div",null,Object(ce.jsx)("h4",null,"Performance"),Object(ce.jsx)("p",{className:"helper"},"Adjust performance settings of this database.")),key:"2"},Object(ce.jsx)(Re,{className:"mb-8"},Object(ce.jsx)("div",{className:"control-label"},Object(n.e)("Chart cache timeout")),Object(ce.jsx)("div",{className:"input-container"},Object(ce.jsx)("input",{type:"number",name:"cache_timeout",value:(null==e?void 0:e.cache_timeout)||"",placeholder:Object(n.e)("Enter duration in seconds"),onChange:a})),Object(ce.jsx)("div",{className:"helper"},Object(n.e)("Duration (in seconds) of the caching timeout for charts of this database. A timeout of 0 indicates that the cache never expires. Note this defaults to the global timeout if undefined."))),Object(ce.jsx)(Re,null,Object(ce.jsx)("div",{className:"control-label"},Object(n.e)("Schema cache timeout")),Object(ce.jsx)("div",{className:"input-container"},Object(ce.jsx)("input",{type:"number",name:"schema_cache_timeout",value:(null==e?void 0:null==(c=e.extra_json)?void 0:null==(d=c.metadata_cache_timeout)?void 0:d.schema_cache_timeout)||"",placeholder:Object(n.e)("Enter duration in seconds"),onChange:o})),Object(ce.jsx)("div",{className:"helper"},Object(n.e)("Duration (in seconds) of the metadata caching timeout for schemas of this database. If left unset, the cache never expires."))),Object(ce.jsx)(Re,null,Object(ce.jsx)("div",{className:"control-label"},Object(n.e)("Table cache timeout")),Object(ce.jsx)("div",{className:"input-container"},Object(ce.jsx)("input",{type:"number",name:"table_cache_timeout",value:(null==e?void 0:null==(p=e.extra_json)?void 0:null==(b=p.metadata_cache_timeout)?void 0:b.table_cache_timeout)||"",placeholder:Object(n.e)("Enter duration in seconds"),onChange:o})),Object(ce.jsx)("div",{className:"helper"},Object(n.e)("Duration (in seconds) of the metadata caching timeout for tables of this database. If left unset, the cache never expires. "))),Object(ce.jsx)(Re,{css:Object(ce.css)({no_margin_bottom:_e},"","")},Object(ce.jsx)("div",{className:"input-container"},Object(ce.jsx)(ve.a,{id:"allow_run_async",indeterminate:!1,checked:!(null==e||!e.allow_run_async),onChange:a,labelText:Object(n.e)("Asynchronous query execution")}),Object(ce.jsx)(ge.a,{tooltip:Object(n.e)("Operate the database in asynchronous mode, meaning that the queries are executed on remote workers as opposed to on the web server itself. This assumes that you have a Celery worker setup as well as a results backend. Refer to the installation docs for more information.")}))),Object(ce.jsx)(Re,{css:Object(ce.css)({no_margin_bottom:_e},"","")},Object(ce.jsx)("div",{className:"input-container"},Object(ce.jsx)(ve.a,{id:"cancel_query_on_windows_unload",indeterminate:!1,checked:!(null==e||null==(u=e.extra_json)||!u.cancel_query_on_windows_unload),onChange:o,labelText:Object(n.e)("Cancel query on window unload event")}),Object(ce.jsx)(ge.a,{tooltip:Object(n.e)("Terminate running queries when browser window closed or navigated to another page. Available for Presto, Hive, MySQL, Postgres and Snowflake databases.")})))),Object(ce.jsx)(ye.a.Panel,{header:Object(ce.jsx)("div",null,Object(ce.jsx)("h4",null,"Security"),Object(ce.jsx)("p",{className:"helper"},"Add extra connection information.")),key:"3"},Object(ce.jsx)(Re,null,Object(ce.jsx)("div",{className:"control-label"},Object(n.e)("Secure extra")),Object(ce.jsx)("div",{className:"input-container"},Object(ce.jsx)(De,{name:"encrypted_extra",value:(null==e?void 0:e.encrypted_extra)||"",placeholder:Object(n.e)("Secure extra"),onChange:e=>s({json:e,name:"encrypted_extra"}),width:"100%",height:"160px"})),Object(ce.jsx)("div",{className:"helper"},Object(ce.jsx)("div",null,Object(n.e)("JSON string containing additional connection configuration. This is used to provide connection information for systems like Hive, Presto and BigQuery which do not conform to the username:password syntax normally used by SQLAlchemy.")))),Object(ce.jsx)(Re,null,Object(ce.jsx)("div",{className:"control-label"},Object(n.e)("Root certificate")),Object(ce.jsx)("div",{className:"input-container"},Object(ce.jsx)("textarea",{name:"server_cert",value:(null==e?void 0:e.server_cert)||"",placeholder:Object(n.e)("Enter CA_BUNDLE"),onChange:t})),Object(ce.jsx)("div",{className:"helper"},Object(n.e)("Optional CA_BUNDLE contents to validate HTTPS requests. Only available on certain database engines."))),Object(ce.jsx)(Re,null,Object(ce.jsx)("div",{className:"control-label"},Object(n.e)("Schemas allowed for CSV upload")),Object(ce.jsx)("div",{className:"input-container"},Object(ce.jsx)("input",{type:"text",name:"schemas_allowed_for_csv_upload",value:((null==e?void 0:null==(h=e.extra_json)?void 0:h.schemas_allowed_for_csv_upload)||[]).join(","),placeholder:"schema1,schema2",onChange:o})),Object(ce.jsx)("div",{className:"helper"},Object(n.e)("A comma-separated list of schemas that CSVs are allowed to upload to."))),Object(ce.jsx)(Re,{css:Object(ce.css)({no_margin_bottom:_e},"","")},Object(ce.jsx)("div",{className:"input-container"},Object(ce.jsx)(ve.a,{id:"impersonate_user",indeterminate:!1,checked:!(null==e||!e.impersonate_user),onChange:a,labelText:Object(n.e)("Impersonate logged in user (Presto, Trino, Hive, and GSheets)")}),Object(ce.jsx)(ge.a,{tooltip:Object(n.e)("If Presto or Trino, all the queries in SQL Lab are going to be executed as the currently logged on user who must have permission to run them. If Hive and hive.server2.enable.doAs is enabled, will run the queries as service account, but impersonate the currently logged on user via hive.server2.proxy.user property.")}))),Object(ce.jsx)(Re,{css:Object(ce.css)({..._e},"","")},Object(ce.jsx)("div",{className:"input-container"},Object(ce.jsx)(ve.a,{id:"allow_csv_upload",indeterminate:!1,checked:!(null==e||!e.allow_csv_upload),onChange:a,labelText:Object(n.e)("Allow data upload")}),Object(ce.jsx)(ge.a,{tooltip:Object(n.e)("If selected, please set the schemas allowed for data upload in Extra.")})))),Object(ce.jsx)(ye.a.Panel,{header:Object(ce.jsx)("div",null,Object(ce.jsx)("h4",null,"Other"),Object(ce.jsx)("p",{className:"helper"},"Additional settings.")),key:"4"},Object(ce.jsx)(Re,null,Object(ce.jsx)("div",{className:"control-label"},Object(n.e)("Metadata Parameters")),Object(ce.jsx)("div",{className:"input-container"},Object(ce.jsx)(De,{name:"metadata_params",value:(null==e?void 0:null==(m=e.extra_json)?void 0:m.metadata_params)||"",placeholder:Object(n.e)("Metadata Parameters"),onChange:e=>l({json:e,name:"metadata_params"}),width:"100%",height:"160px"})),Object(ce.jsx)("div",{className:"helper"},Object(ce.jsx)("div",null,Object(n.e)("The metadata_params object gets unpacked into the sqlalchemy.MetaData call.")))),Object(ce.jsx)(Re,null,Object(ce.jsx)("div",{className:"control-label"},Object(n.e)("Engine Parameters")),Object(ce.jsx)("div",{className:"input-container"},Object(ce.jsx)(De,{name:"engine_params",value:(null==e?void 0:null==(g=e.extra_json)?void 0:g.engine_params)||"",placeholder:Object(n.e)("Engine Parameters"),onChange:e=>l({json:e,name:"engine_params"}),width:"100%",height:"160px"})),Object(ce.jsx)("div",{className:"helper"},Object(ce.jsx)("div",null,Object(n.e)("The engine_params object gets unpacked into the sqlalchemy.create_engine call.")))),Object(ce.jsx)(Re,null,Object(ce.jsx)("div",{className:"control-label"},Object(n.e)("Version")),Object(ce.jsx)("div",{className:"input-container"},Object(ce.jsx)("input",{type:"number",name:"version",value:(null==e?void 0:null==(j=e.extra_json)?void 0:j.version)||"",placeholder:Object(n.e)("Version number"),onChange:o})),Object(ce.jsx)("div",{className:"helper"},Object(n.e)("Specify the database version. This should be used with Presto in order to enable query cost estimation.")))))};var Xe=({db:e,onInputChange:a,testConnection:t,conf:s,isEditMode:o=!1})=>{var l,r;return Object(ce.jsx)(i.a.Fragment,null,Object(ce.jsx)(Re,null,Object(ce.jsx)("div",{className:"control-label"},Object(n.e)("Display Name"),Object(ce.jsx)("span",{className:"required"},"*")),Object(ce.jsx)("div",{className:"input-container"},Object(ce.jsx)("input",{type:"text",name:"database_name",value:(null==e?void 0:e.database_name)||"",placeholder:Object(n.e)("Name your database"),onChange:a})),Object(ce.jsx)("div",{className:"helper"},Object(n.e)("Pick a name to help you identify this database."))),Object(ce.jsx)(Re,null,Object(ce.jsx)("div",{className:"control-label"},Object(n.e)("SQLAlchemy URI"),Object(ce.jsx)("span",{className:"required"},"*")),Object(ce.jsx)("div",{className:"input-container"},Object(ce.jsx)("input",{type:"text",name:"sqlalchemy_uri",value:(null==e?void 0:e.sqlalchemy_uri)||"",autoComplete:"off",placeholder:Object(n.e)("dialect+driver://username:password@host:port/database"),onChange:a})),Object(ce.jsx)("div",{className:"helper"},Object(n.e)("Refer to the")," ",Object(ce.jsx)("a",{href:null!=(l=null==s?void 0:s.SQLALCHEMY_DOCS_URL)?l:"",target:"_blank",rel:"noopener noreferrer"},null!=(r=null==s?void 0:s.SQLALCHEMY_DISPLAY_TEXT)?r:"")," ",Object(n.e)("for more information on how to structure your URI."))),Object(ce.jsx)(ee.a,{onClick:t,cta:!0,buttonStyle:"link",css:e=>(e=>ce.css`
  width: 100%;
  border: 1px solid ${e.colors.primary.dark2};
  color: ${e.colors.primary.dark2};
  &:hover,
  &:focus {
    border: 1px solid ${e.colors.primary.dark1};
    color: ${e.colors.primary.dark1};
  }
`)(e)},Object(n.e)("Test connection")))},Ke=t(32),Ze=t.n(Ke),ea=t(467),aa=t(350),ta={icon:{tag:"svg",attrs:{viewBox:"64 64 896 896",focusable:"false"},children:[{tag:"path",attrs:{d:"M864 256H736v-80c0-35.3-28.7-64-64-64H352c-35.3 0-64 28.7-64 64v80H160c-17.7 0-32 14.3-32 32v32c0 4.4 3.6 8 8 8h60.4l24.7 523c1.6 34.1 29.8 61 63.9 61h454c34.2 0 62.3-26.8 63.9-61l24.7-523H888c4.4 0 8-3.6 8-8v-32c0-17.7-14.3-32-32-32zm-200 0H360v-72h304v72z"}}]},name:"delete",theme:"filled"},na=t(1583),sa=function(e,a){return l.createElement(na.a,Object.assign({},e,{ref:a,icon:ta}))};sa.displayName="DeleteFilled";var oa=l.forwardRef(sa),la={icon:{tag:"svg",attrs:{viewBox:"64 64 896 896",focusable:"false"},children:[{tag:"path",attrs:{d:"M563.8 512l262.5-312.9c4.4-5.2.7-13.1-6.1-13.1h-79.8c-4.7 0-9.2 2.1-12.3 5.7L511.6 449.8 295.1 191.7c-3-3.6-7.5-5.7-12.3-5.7H203c-6.8 0-10.5 7.9-6.1 13.1L459.4 512 196.9 824.9A7.95 7.95 0 00203 838h79.8c4.7 0 9.2-2.1 12.3-5.7l216.5-258.1 216.5 258.1c3 3.6 7.5 5.7 12.3 5.7h79.8c6.8 0 10.5-7.9 6.1-13.1L563.8 512z"}}]},name:"close",theme:"outlined"},ia=function(e,a){return l.createElement(na.a,Object.assign({},e,{ref:a,icon:la}))};ia.displayName="CloseOutlined";var ra,ca=l.forwardRef(ia);!function(e){e[e.jsonUpload=0]="jsonUpload",e[e.copyPaste=1]="copyPaste"}(ra||(ra={}));const da=["host","port","database","username","password","database_name","credentials_info","catalog","query","encryption"];var pa={name:"s5xdrg",styles:"display:flex;align-items:center"};const ba={host:({required:e,changeMethods:a,getValidation:t,validationErrors:s,db:o})=>{var l;return Object(ce.jsx)(ea.a,{id:"host",name:"host",value:null==o?void 0:null==(l=o.parameters)?void 0:l.host,required:e,hasTooltip:!0,tooltipText:Object(n.e)("This can be either an IP address (e.g. 127.0.0.1) or a domain name (e.g. mydatabase.com)."),validationMethods:{onBlur:t},errorMessage:null==s?void 0:s.host,placeholder:"e.g. 127.0.0.1",className:"form-group-w-50",label:"Host",onChange:a.onParametersChange})},port:({required:e,changeMethods:a,getValidation:t,validationErrors:n,db:s})=>{var o;return Object(ce.jsx)(i.a.Fragment,null,Object(ce.jsx)(ea.a,{id:"port",name:"port",type:"number",required:e,value:null==s?void 0:null==(o=s.parameters)?void 0:o.port,validationMethods:{onBlur:t},errorMessage:null==n?void 0:n.port,placeholder:"e.g. 5432",className:"form-group-w-50",label:"Port",onChange:a.onParametersChange}))},database:({required:e,changeMethods:a,getValidation:t,validationErrors:s,db:o})=>{var l;return Object(ce.jsx)(ea.a,{id:"database",name:"database",required:e,value:null==o?void 0:null==(l=o.parameters)?void 0:l.database,validationMethods:{onBlur:t},errorMessage:null==s?void 0:s.database,placeholder:"e.g. world_population",label:"Database name",onChange:a.onParametersChange,helpText:Object(n.e)("Copy the name of the  database you are trying to connect to.")})},username:({required:e,changeMethods:a,getValidation:t,validationErrors:n,db:s})=>{var o;return Object(ce.jsx)(ea.a,{id:"username",name:"username",required:e,value:null==s?void 0:null==(o=s.parameters)?void 0:o.username,validationMethods:{onBlur:t},errorMessage:null==n?void 0:n.username,placeholder:"e.g. Analytics",label:"Username",onChange:a.onParametersChange})},password:({required:e,changeMethods:a,getValidation:t,validationErrors:n,db:s,isEditMode:o})=>{var l;return Object(ce.jsx)(ea.a,{id:"password",name:"password",required:e,type:o&&"password",value:null==s?void 0:null==(l=s.parameters)?void 0:l.password,validationMethods:{onBlur:t},errorMessage:null==n?void 0:n.password,placeholder:"e.g. ********",label:"Password",onChange:a.onParametersChange})},database_name:({changeMethods:e,getValidation:a,validationErrors:t,db:s})=>Object(ce.jsx)(i.a.Fragment,null,Object(ce.jsx)(ea.a,{id:"database_name",name:"database_name",required:!0,value:null==s?void 0:s.database_name,validationMethods:{onBlur:a},errorMessage:null==t?void 0:t.database_name,placeholder:"",label:Object(n.e)("Display Name"),onChange:e.onChange,helpText:Object(n.e)("Pick a nickname for this database to display as in Superset.")})),query:({required:e,changeMethods:a,getValidation:t,validationErrors:s,db:o})=>Object(ce.jsx)(ea.a,{id:"query_input",name:"query_input",required:e,value:(null==o?void 0:o.query_input)||"",validationMethods:{onBlur:t},errorMessage:null==s?void 0:s.query,placeholder:"e.g. param1=value1&param2=value2",label:"Additional Parameters",onChange:a.onQueryChange,helpText:Object(n.e)("Add additional custom parameters")}),encryption:({isEditMode:e,changeMethods:a,db:t,sslForced:s})=>{var o;return Object(ce.jsx)("div",{css:e=>Ne(e)},Object(ce.jsx)(X.x,{disabled:s&&!e,checked:(null==t?void 0:null==(o=t.parameters)?void 0:o.encryption)||s,onChange:e=>{a.onParametersChange({target:{type:"toggle",name:"encryption",checked:!0,value:e}})}}),Object(ce.jsx)("span",{css:Ee},"SSL"),Object(ce.jsx)(ge.a,{tooltip:Object(n.e)('SSL Mode "require" will be used.'),placement:"right",viewBox:"0 -5 24 24"}))},credentials_info:({changeMethods:e,isEditMode:a,db:t,editNewDb:s})=>{var o;const[r,c]=Object(l.useState)(ra.jsonUpload.valueOf()),[d,p]=Object(l.useState)(null);return Object(ce.jsx)(Qe,null,!a&&Object(ce.jsx)(i.a.Fragment,null,Object(ce.jsx)(aa.a,{required:!0},Object(n.e)("How do you want to enter service account credentials?")),Object(ce.jsx)(X.u,{defaultValue:r,style:{width:"100%"},onChange:e=>c(e)},Object(ce.jsx)(X.u.Option,{value:ra.jsonUpload},Object(n.e)("Upload JSON file")),Object(ce.jsx)(X.u.Option,{value:ra.copyPaste},Object(n.e)("Copy and Paste JSON credentials")))),r===ra.copyPaste||a||s?Object(ce.jsx)("div",{className:"input-container"},Object(ce.jsx)(aa.a,{required:!0},Object(n.e)("Service Account")),Object(ce.jsx)("textarea",{className:"input-form",name:"credentials_info",value:null==t?void 0:null==(o=t.parameters)?void 0:o.credentials_info,onChange:e.onParametersChange,placeholder:"Paste content of service credentials JSON file here"}),Object(ce.jsx)("span",{className:"label-paste"},Object(n.e)("Copy and paste the entire service account .json file here"))):Object(ce.jsx)("div",{className:"input-container",css:e=>Ne(e)},Object(ce.jsx)("div",{css:pa},Object(ce.jsx)(aa.a,{required:!0},Object(n.e)("Upload Credentials")),Object(ce.jsx)(ge.a,{tooltip:Object(n.e)("Use the JSON file you automatically downloaded when creating your service account in Google BigQuery."),viewBox:"0 0 24 24"})),!d&&Object(ce.jsx)(X.e,{className:"input-upload-btn",onClick:()=>{var e,a;return null==(e=document)?void 0:null==(a=e.getElementById("selectedFile"))?void 0:a.click()}},Object(n.e)("Choose File")),d&&Object(ce.jsx)("div",{className:"input-upload-current"},d,Object(ce.jsx)(oa,{onClick:()=>{p(null),e.onParametersChange({target:{name:"credentials_info",value:""}})}})),Object(ce.jsx)("input",{id:"selectedFile",className:"input-upload",type:"file",onChange:async a=>{var t,n;let s;a.target.files&&(s=a.target.files[0]),p(null==(t=s)?void 0:t.name),e.onParametersChange({target:{type:null,name:"credentials_info",value:await(null==(n=s)?void 0:n.text()),checked:!1}}),document.getElementById("selectedFile").value=null}})))},catalog:({required:e,changeMethods:a,getValidation:t,validationErrors:s,db:o})=>{const l=(null==o?void 0:o.catalog)||[],r=s||{};return Object(ce.jsx)(We,null,Object(ce.jsx)("div",{className:"catalog-type-select"},Object(ce.jsx)(aa.a,{required:!0},Object(n.e)("Type of Google Sheets Allowed")),Object(ce.jsx)(X.u,{style:{width:"100%"},defaultValue:"true",disabled:!0},Object(ce.jsx)(X.u.Option,{value:"true",key:1},Object(n.e)("Publicly shared sheets only")))),Object(ce.jsx)("h4",{className:"gsheet-title"},Object(n.e)("Connect Google Sheets as tables to this database")),Object(ce.jsx)("div",null,null==l?void 0:V()(l).call(l,(s,o)=>Object(ce.jsx)(i.a.Fragment,null,Object(ce.jsx)(aa.a,{className:"catalog-label",required:!0},Object(n.e)("Google Sheet Name and URL")),Object(ce.jsx)("div",{className:"catalog-name"},Object(ce.jsx)(X.m,{className:"catalog-name-input",placeholder:Object(n.e)("Enter a name for this sheet"),onChange:e=>{a.onParametersChange({target:{type:`catalog-${o}`,name:"name",value:e.target.value}})},value:s.name}),(null==l?void 0:l.length)>1&&Object(ce.jsx)(ca,{className:"catalog-delete",onClick:()=>a.onRemoveTableCatalog(o)})),Object(ce.jsx)(ea.a,{className:"catalog-name-url",required:e,validationMethods:{onBlur:t},errorMessage:r[s.name],placeholder:Object(n.e)("Paste the shareable Google Sheet URL here"),onChange:e=>a.onParametersChange({target:{type:`catalog-${o}`,name:"value",value:e.target.value}}),value:s.value}))),Object(ce.jsx)(Ye,{className:"catalog-add-btn",onClick:()=>{a.onAddTableCatalog()}},"+ ",Object(n.e)("Add sheet"))))}};var ua=({dbModel:{parameters:e},onParametersChange:a,onChange:t,onQueryChange:n,onParametersUploadFileChange:s,onAddTableCatalog:o,onRemoveTableCatalog:l,validationErrors:r,getValidation:c,db:d,isEditMode:p=!1,sslForced:b,editNewDb:u})=>{var h;return Object(ce.jsx)(i.a.Fragment,null,Object(ce.jsx)("div",{css:e=>[Se,qe(e)]},e&&V()(h=A()(da).call(da,a=>{var t;return Ze()(t=L()(e.properties)).call(t,a)||"database_name"===a})).call(h,i=>{var h;return ba[i]({required:null==(h=e.required)?void 0:Ze()(h).call(h,i),changeMethods:{onParametersChange:a,onChange:t,onQueryChange:n,onParametersUploadFileChange:s,onAddTableCatalog:o,onRemoveTableCatalog:l},validationErrors:r,getValidation:c,db:d,key:i,isEditMode:p,sslForced:b,editNewDb:u})})))};const ha=Object(d.c)(),ma=ha?ha.support:"https://superset.apache.org/docs/databases/installing-database-drivers",ga={postgresql:"https://superset.apache.org/docs/databases/postgres",mssql:"https://superset.apache.org/docs/databases/sql-server",gsheets:"https://superset.apache.org/docs/databases/google-sheets"},ja=e=>e?ha?ha[e]||ha.default:ga[e]?ga[e]:`https://superset.apache.org/docs/databases/${e}`:null;var xa=({isLoading:e,isEditMode:a,useSqlAlchemyForm:t,hasConnectedDb:n,db:s,dbName:o,dbModel:l,editNewDb:r})=>{const c=Object(ce.jsx)(Ce,null,Object(ce.jsx)(He,null,null==s?void 0:s.backend),Object(ce.jsx)(Be,null,o)),d=Object(ce.jsx)(Ce,null,Object(ce.jsx)("p",{className:"helper-top"}," STEP 2 OF 2 "),Object(ce.jsx)("h4",null,"Enter Primary Credentials"),Object(ce.jsx)("p",{className:"helper-bottom"},"Need help? Learn how to connect your database"," ",Object(ce.jsx)("a",{href:(null==ha?void 0:ha.default)||ma,target:"_blank",rel:"noopener noreferrer"},"here"),".")),p=Object(ce.jsx)(Je,null,Object(ce.jsx)(Ce,null,Object(ce.jsx)("p",{className:"helper-top"}," STEP 3 OF 3 "),Object(ce.jsx)("h4",{className:"step-3-text"},"Your database was successfully connected! Here are some optional settings for your database"),Object(ce.jsx)("p",{className:"helper-bottom"},"Need help? Learn more about"," ",Object(ce.jsx)("a",{href:ja(null==s?void 0:s.engine),target:"_blank",rel:"noopener noreferrer"},"connecting to ",l.name,".")))),b=Object(ce.jsx)(Je,null,Object(ce.jsx)(Ce,null,Object(ce.jsx)("p",{className:"helper-top"}," STEP 2 OF 3 "),Object(ce.jsx)("h4",null,"Enter the required ",l.name," credentials"),Object(ce.jsx)("p",{className:"helper-bottom"},"Need help? Learn more about"," ",Object(ce.jsx)("a",{href:ja(null==s?void 0:s.engine),target:"_blank",rel:"noopener noreferrer"},"connecting to ",l.name,".")))),u=Object(ce.jsx)(Ce,null,Object(ce.jsx)("div",{className:"select-db"},Object(ce.jsx)("p",{className:"helper-top"}," STEP 1 OF 3 "),Object(ce.jsx)("h4",null,"Select a database to connect")));return e?Object(ce.jsx)(i.a.Fragment,null):a?c:t?d:n&&!r?p:s||r?b:u};const Oa={gsheets:{message:"Why do I need to create a database?",description:"To begin using your Google Sheets, you need to create a database first. Databases are used as a way to identify your data so that it can be queried and visualized. This database will hold all of your individual Google Sheets you choose to connect here."}},va={CONNECTION_MISSING_PARAMETERS_ERROR:{message:"Missing Required Fields",description:"Please complete all required fields."},CONNECTION_INVALID_HOSTNAME_ERROR:{message:"Could not verify the host",description:"The host is invalid. Please verify that this field is entered correctly."},CONNECTION_PORT_CLOSED_ERROR:{message:"Port is closed",description:"Please verify that port is open to connect."},CONNECTION_INVALID_PORT_ERROR:{message:"Invalid Port Number",description:"The port must be a whole number less than or equal to 65535."},CONNECTION_ACCESS_DENIED_ERROR:{message:"Invalid account information",description:"Either the username or password is incorrect."},CONNECTION_INVALID_PASSWORD_ERROR:{message:"Invalid account information",description:"Either the username or password is incorrect."},INVALID_PAYLOAD_SCHEMA_ERROR:{message:"Incorrect Fields",description:"Please make sure all fields are filled out correctly"},TABLE_DOES_NOT_EXIST_ERROR:{message:"URL could not be identified",description:'The URL could not be identified. Please check for typos and make sure that "Type of google sheet allowed" selection matches the input'}};var ya;function fa(e,a){var t,n,s,o,l,i,r;const c={...e||{}};let d,p={},b="",u={};switch(a.type){case ya.extraEditorChange:return{...c,extra_json:{...c.extra_json,[a.payload.name]:a.payload.json}};case ya.extraInputChange:var h;return"schema_cache_timeout"===a.payload.name||"table_cache_timeout"===a.payload.name?{...c,extra_json:{...c.extra_json,metadata_cache_timeout:{...null==(h=c.extra_json)?void 0:h.metadata_cache_timeout,[a.payload.name]:a.payload.value}}}:"schemas_allowed_for_csv_upload"===a.payload.name?{...c,extra_json:{...c.extra_json,schemas_allowed_for_csv_upload:(a.payload.value||"").split(",")}}:{...c,extra_json:{...c.extra_json,[a.payload.name]:"checkbox"===a.payload.type?a.payload.checked:a.payload.value}};case ya.inputChange:return"checkbox"===a.payload.type?{...c,[a.payload.name]:a.payload.checked}:{...c,[a.payload.name]:a.payload.value};case ya.parametersChange:if(void 0!==c.catalog&&null!=(t=a.payload.type)&&J()(t).call(t,"catalog")){var m,g;const e=null==(m=a.payload.type)?void 0:m.split("-")[1];((null==c?void 0:c.catalog[e])||{})[a.payload.name]=a.payload.value;const t={};return null==(g=c.catalog)||V()(g).call(g,e=>{t[e.name]=e.value}),{...c,parameters:{...c.parameters,catalog:t}}}return{...c,parameters:{...c.parameters,[a.payload.name]:a.payload.value}};case ya.addTableCatalogSheet:return void 0!==c.catalog?{...c,catalog:[...c.catalog,{name:"",value:""}]}:{...c,catalog:[{name:"",value:""}]};case ya.removeTableCatalogSheet:return null==(n=c.catalog)||B()(n).call(n,a.payload.indexToDelete,1),{...c};case ya.editorChange:return{...c,[a.payload.name]:a.payload.json};case ya.queryChange:return{...c,parameters:{...c.parameters,query:F()(new P.a(a.payload.value))},query_input:a.payload.value};case ya.textChange:return{...c,[a.payload.name]:a.payload.value};case ya.fetched:var j,x,O,v,y;if(a.payload.extra)d={...JSON.parse(a.payload.extra||"")},u={...JSON.parse(a.payload.extra||""),metadata_params:D()(null==(j=d)?void 0:j.metadata_params),engine_params:D()(null==(x=d)?void 0:x.engine_params),schemas_allowed_for_csv_upload:null==(O=d)?void 0:O.schemas_allowed_for_csv_upload};if(p=(null==(s=a.payload)?void 0:null==(o=s.parameters)?void 0:o.query)||{},b=V()(l=q()(p)).call(l,([e,a])=>`${e}=${a}`).join("&"),"bigquery"===a.payload.backend&&a.payload.configuration_method===he.DYNAMIC_FORM)return{...a.payload,engine:a.payload.backend,configuration_method:a.payload.configuration_method,extra_json:u,parameters:{credentials_info:D()((null==(v=a.payload)?void 0:null==(y=v.parameters)?void 0:y.credentials_info)||""),query:p},query_input:b};if("gsheets"===a.payload.backend&&a.payload.configuration_method===he.DYNAMIC_FORM&&void 0!==(null==(i=d)?void 0:null==(r=i.engine_params)?void 0:r.catalog)){var f,_,C;const e=null==(f=d)?void 0:null==(_=f.engine_params)?void 0:_.catalog;return{...a.payload,engine:a.payload.backend,configuration_method:a.payload.configuration_method,extra_json:u,catalog:V()(C=L()(e)).call(C,a=>({name:a,value:e[a]})),query_input:b}}return{...a.payload,encrypted_extra:a.payload.encrypted_extra||"",engine:a.payload.backend||c.engine,configuration_method:a.payload.configuration_method,extra_json:u,parameters:a.payload.parameters,query_input:b};case ya.dbSelected:case ya.configMethodChange:return{...a.payload};case ya.reset:default:return null}}!function(e){e[e.configMethodChange=0]="configMethodChange",e[e.dbSelected=1]="dbSelected",e[e.editorChange=2]="editorChange",e[e.fetched=3]="fetched",e[e.inputChange=4]="inputChange",e[e.parametersChange=5]="parametersChange",e[e.reset=6]="reset",e[e.textChange=7]="textChange",e[e.extraInputChange=8]="extraInputChange",e[e.extraEditorChange=9]="extraEditorChange",e[e.addTableCatalogSheet=10]="addTableCatalogSheet",e[e.removeTableCatalogSheet=11]="removeTableCatalogSheet",e[e.queryChange=12]="queryChange"}(ya||(ya={}));const _a=e=>{var a;return D()({...e,metadata_params:JSON.parse((null==e?void 0:e.metadata_params)||"{}"),engine_params:JSON.parse((null==e?void 0:e.engine_params)||"{}"),schemas_allowed_for_csv_upload:A()(a=(null==e?void 0:e.schemas_allowed_for_csv_upload)||[]).call(a,e=>""!==e)})};var Ca=Object(b.a)(({addDangerToast:e,addSuccessToast:a,onDatabaseAdd:t,onHide:s,show:o,databaseId:c})=>{var p;const[b,u]=Object(l.useReducer)(fa,null),[h,m]=Object(l.useState)("1"),[g,j]=Object(d.f)(),[x,O,v]=Object(d.h)(),[y,_]=Object(l.useState)(!1),[w,N]=Object(l.useState)(""),[S,T]=Object(l.useState)(!1),[U,M]=Object(l.useState)(!1),R=Object(je.d)(e=>e.common.conf),I=Object(d.d)(),P=Object(d.b)(),z=!!c,F=Object(W.b)(W.a.FORCE_DATABASE_CONNECTIONS_SSL),H=P||!(null==b||!b.engine||!Oa[b.engine]),B=(null==b?void 0:b.configuration_method)===he.SQLALCHEMY_URI,Q=z||B,{state:{loading:Y,resource:J,error:ae},fetchResource:te,createResource:ne,updateResource:se,clearError:oe}=Object(d.l)("database",Object(n.e)("database"),e),le=x||ae,ie=e=>e&&0===L()(e).length,re=(null==g?void 0:null==(p=g.databases)?void 0:k()(p).call(p,e=>e.engine===(z?null==b?void 0:b.backend:null==b?void 0:b.engine)))||{},de=()=>{u({type:ya.reset}),_(!1),v(null),oe(),T(!1),s()},pe=async()=>{var e;const{id:a,...n}=b||{},s=JSON.parse(D()(n));if(s.configuration_method===he.DYNAMIC_FORM){var o;if(await O(s,!0),x&&!ie(x))return;var l,i,r,c,d;if("bigquery"===(s.backend||s.engine)&&null!=(o=s.parameters)&&o.credentials_info)if(null!=(l=s.parameters)&&l.credentials_info&&"object"==typeof(null==(i=s.parameters)?void 0:i.credentials_info)&&(null==(r=s.parameters)?void 0:r.credentials_info.constructor)===Object)s.encrypted_extra=D()({credentials_info:null==(c=s.parameters)?void 0:c.credentials_info}),s.parameters.credentials_info=D()(s.parameters.credentials_info);else s.encrypted_extra=D()({credentials_info:JSON.parse(null==(d=s.parameters)?void 0:d.credentials_info)})}if(null!=s&&null!=(e=s.parameters)&&e.catalog&&(s.extra_json={engine_params:D()({catalog:s.parameters.catalog})}),null!=s&&s.extra_json&&(s.extra=_a(null==s?void 0:s.extra_json)),null!=b&&b.id){M(!0),await se(b.id,s,s.configuration_method===he.DYNAMIC_FORM)&&(t&&t(),S||de())}else if(b){M(!0),await ne(s,s.configuration_method===he.DYNAMIC_FORM)&&(_(!0),t&&t(),Q&&de())}T(!1),M(!1)},be=(e,a)=>{u({type:e,payload:a})},ue=e=>{var a;const t=null==g?void 0:A()(a=g.databases).call(a,a=>a.name===e)[0],{engine:n,parameters:s}=t,o=void 0!==s;u({type:ya.dbSelected,payload:{database_name:e,configuration_method:o?he.DYNAMIC_FORM:he.SQLALCHEMY_URI,engine:n}}),u({type:ya.addTableCatalogSheet})},xe=()=>{J&&te(J.id),T(!0)},Oe=()=>{S&&_(!1),u({type:ya.reset})},ve=()=>b?!y||S?Object(ce.jsx)(i.a.Fragment,null,Object(ce.jsx)(Ye,{key:"back",onClick:Oe},"Back"),Object(ce.jsx)(Ye,{key:"submit",buttonStyle:"primary",onClick:pe},"Connect")):Object(ce.jsx)(i.a.Fragment,null,Object(ce.jsx)(Ye,{key:"back",onClick:xe},"Back"),Object(ce.jsx)(Ye,{key:"submit",buttonStyle:"primary",onClick:pe},"Finish")):[];Object(l.useEffect)(()=>{o&&(m("1"),j(),M(!0)),c&&o&&z&&c&&(Y||te(c).catch(a=>e(Object(n.e)("Sorry there was an error fetching database information: %s",a.message))))},[o,c]),Object(l.useEffect)(()=>{J&&(u({type:ya.fetched,payload:J}),N(J.database_name))},[J]),Object(l.useEffect)(()=>{U&&M(!1)},[g]);const ye=()=>{if(ie(ae)||ie(x)&&!((null==x?void 0:x.error_type)in va))return Object(ce.jsx)(i.a.Fragment,null);var e,a;if(x)return Object(ce.jsx)(K.a,{type:"error",css:e=>Ue(e),message:(null==(e=va[null==x?void 0:x.error_type])?void 0:e.message)||(null==x?void 0:x.error_type),description:(null==(a=va[null==x?void 0:x.error_type])?void 0:a.description)||D()(x),showIcon:!0,closable:!1});const t=f()(ae);return Object(ce.jsx)(K.a,{type:"error",css:e=>Ue(e),message:"Database Creation Error",description:t[0]})};return Q?Object(ce.jsx)(Z.b,{css:e=>[we,$e,ke(e),Le(e),Me(e)],name:"database",onHandledPrimaryAction:pe,onHide:de,primaryButtonName:z?Object(n.e)("Save"):Object(n.e)("Connect"),width:"500px",centered:!0,show:o,title:Object(ce.jsx)("h4",null,z?Object(n.e)("Edit database"):Object(n.e)("Connect a database")),footer:z?Object(ce.jsx)(i.a.Fragment,null,Object(ce.jsx)(Ye,{key:"close",onClick:de},"Close"),Object(ce.jsx)(Ye,{key:"submit",buttonStyle:"primary",onClick:pe},"Finish")):ve()},Object(ce.jsx)(Je,null,Object(ce.jsx)(Fe,null,Object(ce.jsx)(xa,{isLoading:U,isEditMode:z,useSqlAlchemyForm:B,hasConnectedDb:y,db:b,dbName:w,dbModel:re}))),Object(ce.jsx)(G.c,{defaultActiveKey:"1",activeKey:h,onTabClick:e=>{m(e)},animated:{inkBar:!0,tabPane:!0}},Object(ce.jsx)(G.c.TabPane,{tab:Object(ce.jsx)("span",null,Object(n.e)("Basic")),key:"1"},B?Object(ce.jsx)(Pe,null,Object(ce.jsx)(Xe,{db:b,onInputChange:({target:e})=>be(ya.inputChange,{type:e.type,name:e.name,checked:e.checked,value:e.value}),conf:R,testConnection:()=>{var t;if(null==b||!b.sqlalchemy_uri)return void e(Object(n.e)("Please enter a SQLAlchemy URI to test"));const s={sqlalchemy_uri:(null==b?void 0:b.sqlalchemy_uri)||"",database_name:(null==b?void 0:null==(t=b.database_name)?void 0:E()(t).call(t))||void 0,impersonate_user:(null==b?void 0:b.impersonate_user)||void 0,extra:_a(null==b?void 0:b.extra_json)||void 0,encrypted_extra:(null==b?void 0:b.encrypted_extra)||"",server_cert:(null==b?void 0:b.server_cert)||void 0};Object(d.e)(s,e,a)},isEditMode:z}),(qe=(null==b?void 0:b.backend)||(null==b?void 0:b.engine),void 0!==(null==g?void 0:null==(Re=g.databases)?void 0:null==(De=k()(Re).call(Re,e=>e.backend===qe||e.engine===qe))?void 0:De.parameters)&&!z&&Object(ce.jsx)("div",{css:e=>Ne(e)},Object(ce.jsx)(ee.a,{buttonStyle:"link",onClick:()=>u({type:ya.configMethodChange,payload:{database_name:null==b?void 0:b.database_name,configuration_method:he.DYNAMIC_FORM,engine:null==b?void 0:b.engine}}),css:e=>(e=>ce.css`
  font-weight: 400;
  text-transform: initial;
  padding: ${8*e.gridUnit}px 0 0;
  margin-left: 0px;
`)(e)},"Connect this database using the dynamic form instead"),Object(ce.jsx)(ge.a,{tooltip:Object(n.e)("Click this link to switch to an alternate form that exposes only the required fields needed to connect this database."),viewBox:"0 -6 24 24"})))):Object(ce.jsx)(ua,{isEditMode:!0,sslForced:F,dbModel:re,db:b,onParametersChange:({target:e})=>be(ya.parametersChange,{type:e.type,name:e.name,checked:e.checked,value:e.value}),onChange:({target:e})=>be(ya.textChange,{name:e.name,value:e.value}),onQueryChange:({target:e})=>be(ya.queryChange,{name:e.name,value:e.value}),onAddTableCatalog:()=>u({type:ya.addTableCatalogSheet}),onRemoveTableCatalog:e=>u({type:ya.removeTableCatalogSheet,payload:{indexToDelete:e}}),getValidation:()=>O(b),validationErrors:x}),!z&&Object(ce.jsx)(Ae,null,Object(ce.jsx)(K.a,{closable:!1,css:e=>Te(e),message:"Additional fields may be required",showIcon:!0,description:Object(ce.jsx)(i.a.Fragment,null,"Select databases require additional fields to be completed in the Advanced tab to successfully connect the database. Learn what requirements your databases has"," ",Object(ce.jsx)("a",{href:ma,target:"_blank",rel:"noopener noreferrer",className:"additional-fields-alert-description"},"here"),"."),type:"info"}))),Object(ce.jsx)(G.c.TabPane,{tab:Object(ce.jsx)("span",null,Object(n.e)("Advanced")),key:"2"},Object(ce.jsx)(Ge,{db:b,onInputChange:({target:e})=>be(ya.inputChange,{type:e.type,name:e.name,checked:e.checked,value:e.value}),onTextChange:({target:e})=>be(ya.textChange,{name:e.name,value:e.value}),onEditorChange:e=>be(ya.editorChange,e),onExtraInputChange:({target:e})=>{be(ya.extraInputChange,{type:e.type,name:e.name,checked:e.checked,value:e.value})},onExtraEditorChange:e=>{be(ya.extraEditorChange,e)}}),le&&ye()))):Object(ce.jsx)(Z.b,{css:e=>[$e,ke(e),Le(e),Me(e)],name:"database",onHandledPrimaryAction:pe,onHide:de,primaryButtonName:y?Object(n.e)("Finish"):Object(n.e)("Connect"),width:"500px",centered:!0,show:o,title:Object(ce.jsx)("h4",null,Object(n.e)("Connect a database")),footer:ve()},y?Object(ce.jsx)(i.a.Fragment,null,Object(ce.jsx)(xa,{isLoading:U,isEditMode:z,useSqlAlchemyForm:B,hasConnectedDb:y,db:b,dbName:w,dbModel:re,editNewDb:S}),S?Object(ce.jsx)(ua,{isEditMode:!0,sslForced:F,dbModel:re,db:b,onParametersChange:({target:e})=>be(ya.parametersChange,{type:e.type,name:e.name,checked:e.checked,value:e.value}),onChange:({target:e})=>be(ya.textChange,{name:e.name,value:e.value}),onQueryChange:({target:e})=>be(ya.queryChange,{name:e.name,value:e.value}),onAddTableCatalog:()=>u({type:ya.addTableCatalogSheet}),onRemoveTableCatalog:e=>u({type:ya.removeTableCatalogSheet,payload:{indexToDelete:e}}),getValidation:()=>O(b),validationErrors:x}):Object(ce.jsx)(Ge,{db:b,onInputChange:({target:e})=>be(ya.inputChange,{type:e.type,name:e.name,checked:e.checked,value:e.value}),onTextChange:({target:e})=>be(ya.textChange,{name:e.name,value:e.value}),onEditorChange:e=>be(ya.editorChange,e),onExtraInputChange:({target:e})=>{be(ya.extraInputChange,{type:e.type,name:e.name,checked:e.checked,value:e.value})},onExtraEditorChange:e=>be(ya.extraEditorChange,e)})):Object(ce.jsx)(i.a.Fragment,null,!U&&(b?Object(ce.jsx)(i.a.Fragment,null,Object(ce.jsx)(xa,{isLoading:U,isEditMode:z,useSqlAlchemyForm:B,hasConnectedDb:y,db:b,dbName:w,dbModel:re}),H&&(()=>{var e,a,t,n,s,o;const{hostname:l}=window.location;let i=(null==P?void 0:null==(e=P.REGIONAL_IPS)?void 0:e.default)||"";const r=(null==P?void 0:P.REGIONAL_IPS)||{};return C()(a=q()(r)).call(a,([e,a])=>{e.match(l)&&(i=a)}),(null==b?void 0:b.engine)&&Object(ce.jsx)(Ae,null,Object(ce.jsx)(K.a,{closable:!1,css:e=>Te(e),type:"info",showIcon:!0,message:(null==(t=Oa[b.engine])?void 0:t.message)||(null==P?void 0:null==(n=P.DEFAULT)?void 0:n.message),description:(null==(s=Oa[b.engine])?void 0:s.description)||(null==P?void 0:null==(o=P.DEFAULT)?void 0:o.description)+i}))})(),Object(ce.jsx)(ua,{db:b,sslForced:F,dbModel:re,onAddTableCatalog:()=>{u({type:ya.addTableCatalogSheet})},onQueryChange:({target:e})=>be(ya.queryChange,{name:e.name,value:e.value}),onRemoveTableCatalog:e=>{u({type:ya.removeTableCatalogSheet,payload:{indexToDelete:e}})},onParametersChange:({target:e})=>be(ya.parametersChange,{type:e.type,name:e.name,checked:e.checked,value:e.value}),onChange:({target:e})=>be(ya.textChange,{name:e.name,value:e.value}),getValidation:()=>O(b),validationErrors:x}),Object(ce.jsx)("div",{css:e=>Ne(e)},Object(ce.jsx)(ee.a,{buttonStyle:"link",onClick:()=>u({type:ya.configMethodChange,payload:{engine:b.engine,configuration_method:he.SQLALCHEMY_URI,database_name:b.database_name}}),css:ze},"Connect this database with a SQLAlchemy URI string instead"),Object(ce.jsx)(ge.a,{tooltip:Object(n.e)("Click this link to switch to an alternate form that allows you to input the SQLAlchemy URL for this database manually."),viewBox:"0 -6 24 24"})),le&&ye()):Object(ce.jsx)(Ve,null,Object(ce.jsx)(xa,{isLoading:U,isEditMode:z,useSqlAlchemyForm:B,hasConnectedDb:y,db:b,dbName:w,dbModel:re}),Object(ce.jsx)("div",{className:"preferred"},null==g?void 0:null==(Ee=g.databases)?void 0:V()(Se=A()(Ee).call(Ee,e=>e.preferred)).call(Se,e=>Object(ce.jsx)(me,{className:"preferred-item",onClick:()=>ue(e.name),buttonText:e.name,icon:null==I?void 0:I[e.engine]}))),Object(ce.jsx)("div",{className:"available"},Object(ce.jsx)("h4",{className:"available-label"},"Or choose from a list of other databases we support:"),Object(ce.jsx)("div",{className:"control-label"},"Supported databases"),Object(ce.jsx)(X.u,{className:"available-select",onChange:ue,placeholder:"Choose a database..."},null==(fe=[...(null==g?void 0:g.databases)||[]])?void 0:V()(_e=$()(fe).call(fe,(e,a)=>e.name.localeCompare(a.name))).call(_e,e=>Object(ce.jsx)(X.u.Option,{value:e.name,key:e.name},e.name))),Object(ce.jsx)(K.a,{showIcon:!0,closable:!1,css:e=>Te(e),type:"info",message:(null==P?void 0:null==(Ce=P.ADD_DATABASE)?void 0:Ce.message)||Object(n.e)("Want to add a new database?"),description:null!=P&&P.ADD_DATABASE?Object(ce.jsx)(i.a.Fragment,null,"Any databases that allow connections via SQL Alchemy URIs can be added."," ",Object(ce.jsx)("a",{href:null==P?void 0:P.ADD_DATABASE.contact_link,target:"_blank",rel:"noopener noreferrer"},null==P?void 0:P.ADD_DATABASE.contact_description_link)," ",null==P?void 0:P.ADD_DATABASE.description):Object(ce.jsx)(i.a.Fragment,null,"Any databases that allow connections via SQL Alchemy URIs can be added. Learn about how to connect a database driver"," ",Object(ce.jsx)("a",{href:ma,target:"_blank",rel:"noopener noreferrer"},"here"),".")}))))),U&&Object(ce.jsx)(r.a,null));var fe,_e,Ce,Ee,Se,qe,Re,De});const wa=Object(n.e)('The passwords for the databases below are needed in order to import them. Please note that the "Secure Extra" and "Certificate" sections of the database configuration are not present in export files, and should be added manually after the import if they are needed.'),$a=Object(n.e)("You are importing one or more databases that already exist. Overwriting might cause you to lose some of your work. Are you sure you want to overwrite?"),Na=Object(s.g)(g.a.Check)`
  color: ${({theme:e})=>e.colors.grayscale.dark1};
`,Ea=Object(s.g)(g.a.CancelX)`
  color: ${({theme:e})=>e.colors.grayscale.dark1};
`,Sa=s.g.div`
  color: ${({theme:e})=>e.colors.grayscale.base};
`;function ka({value:e}){return e?Object(ce.jsx)(Na,null):Object(ce.jsx)(Ea,null)}a.default=Object(b.a)((function({addDangerToast:e,addSuccessToast:a}){const{state:{loading:t,resourceCount:s,resourceCollection:b},hasPerm:y,fetchData:f,refreshData:_}=Object(d.k)("database",Object(n.e)("database"),e),[C,w]=Object(l.useState)(!1),[$,N]=Object(l.useState)(null),[E,S]=Object(l.useState)(null),[k,T]=Object(l.useState)(!1),[A,U]=Object(l.useState)([]),[L,M]=Object(l.useState)(!1),q=()=>{T(!0)};function R({database:e=null,modalOpen:a=!1}={}){S(e),w(a)}const D=y("can_write"),I=y("can_write"),P=y("can_write"),z=y("can_read")&&Object(c.c)(c.a.VERSIONED_EXPORT),F={activeChild:"Databases",...x.a};D&&(F.buttons=[{"data-test":"btn-create-database",name:Object(ce.jsx)(i.a.Fragment,null,Object(ce.jsx)("i",{className:"fa fa-plus"})," ",Object(n.e)("Database")," "),buttonStyle:"primary",onClick:()=>{R({modalOpen:!0})}}],Object(c.c)(c.a.VERSIONED_EXPORT)&&F.buttons.push({name:Object(ce.jsx)(m.a,{id:"import-tooltip",title:Object(n.e)("Import databases"),placement:"bottomRight"},Object(ce.jsx)(g.a.Import,null)),buttonStyle:"link",onClick:q}));const H=Object(l.useMemo)(()=>[{accessor:"database_name",Header:Object(n.e)("Database")},{accessor:"backend",Header:Object(n.e)("Backend"),size:"lg",disableSortBy:!0},{accessor:"allow_run_async",Header:Object(ce.jsx)(m.a,{id:"allow-run-async-header-tooltip",title:Object(n.e)("Asynchronous query execution"),placement:"top"},Object(ce.jsx)("span",null,Object(n.e)("AQE"))),Cell:({row:{original:{allow_run_async:e}}})=>Object(ce.jsx)(ka,{value:e}),size:"sm"},{accessor:"allow_dml",Header:Object(ce.jsx)(m.a,{id:"allow-dml-header-tooltip",title:Object(n.e)("Allow data manipulation language"),placement:"top"},Object(ce.jsx)("span",null,Object(n.e)("DML"))),Cell:({row:{original:{allow_dml:e}}})=>Object(ce.jsx)(ka,{value:e}),size:"sm"},{accessor:"allow_csv_upload",Header:Object(n.e)("CSV upload"),Cell:({row:{original:{allow_csv_upload:e}}})=>Object(ce.jsx)(ka,{value:e}),size:"md"},{accessor:"expose_in_sqllab",Header:Object(n.e)("Expose in SQL Lab"),Cell:({row:{original:{expose_in_sqllab:e}}})=>Object(ce.jsx)(ka,{value:e}),size:"md"},{accessor:"created_by",disableSortBy:!0,Header:Object(n.e)("Created by"),Cell:({row:{original:{created_by:e}}})=>e?`${e.first_name} ${e.last_name}`:"",size:"xl"},{Cell:({row:{original:{changed_on_delta_humanized:e}}})=>e,Header:Object(n.e)("Last modified"),accessor:"changed_on_delta_humanized",size:"xl"},{Cell:({row:{original:e}})=>I||P||z?Object(ce.jsx)(Sa,{className:"actions"},P&&Object(ce.jsx)("span",{role:"button",tabIndex:0,className:"action-button",onClick:()=>{return a=e,o.a.get({endpoint:`/api/v1/database/${a.id}/related_objects/`}).then(({json:e={}})=>{N({...a,chart_count:e.charts.count,dashboard_count:e.dashboards.count})}).catch(Object(p.e)(e=>Object(n.e)("An error occurred while fetching database related data: %s",e)));var a}},Object(ce.jsx)(m.a,{id:"delete-action-tooltip",title:Object(n.e)("Delete database"),placement:"bottom"},Object(ce.jsx)(g.a.Trash,null))),z&&Object(ce.jsx)(m.a,{id:"export-action-tooltip",title:Object(n.e)("Export"),placement:"bottom"},Object(ce.jsx)("span",{role:"button",tabIndex:0,className:"action-button",onClick:()=>{var a;void 0!==(a=e).id&&(Object(v.a)("database",[a.id],()=>{M(!1)}),M(!0))}},Object(ce.jsx)(g.a.Share,null))),I&&Object(ce.jsx)(m.a,{id:"edit-action-tooltip",title:Object(n.e)("Edit"),placement:"bottom"},Object(ce.jsx)("span",{role:"button",tabIndex:0,className:"action-button",onClick:()=>R({database:e,modalOpen:!0})},Object(ce.jsx)(g.a.EditAlt,null)))):null,Header:Object(n.e)("Actions"),id:"actions",hidden:!I&&!P,disableSortBy:!0}],[P,I,z]),B=Object(l.useMemo)(()=>[{Header:Object(n.e)("Expose in SQL Lab"),id:"expose_in_sqllab",input:"select",operator:j.a.equals,unfilteredLabel:"All",selects:[{label:"Yes",value:!0},{label:"No",value:!1}]},{Header:Object(ce.jsx)(m.a,{id:"allow-run-async-filter-header-tooltip",title:Object(n.e)("Asynchronous query execution"),placement:"top"},Object(ce.jsx)("span",null,Object(n.e)("AQE"))),id:"allow_run_async",input:"select",operator:j.a.equals,unfilteredLabel:"All",selects:[{label:"Yes",value:!0},{label:"No",value:!1}]},{Header:Object(n.e)("Search"),id:"database_name",input:"search",operator:j.a.contains}],[]);return Object(ce.jsx)(i.a.Fragment,null,Object(ce.jsx)(u.a,F),Object(ce.jsx)(Ca,{databaseId:null==E?void 0:E.id,show:C,onHide:R,onDatabaseAdd:()=>{_()}}),$&&Object(ce.jsx)(h.a,{description:Object(n.e)("The database %s is linked to %s charts that appear on %s dashboards. Are you sure you want to continue? Deleting the database will break those objects.",$.database_name,$.chart_count,$.dashboard_count),onConfirm:()=>{$&&function({id:t,database_name:s}){o.a.delete({endpoint:`/api/v1/database/${t}`}).then(()=>{_(),a(Object(n.e)("Deleted: %s",s)),N(null)},Object(p.e)(a=>e(Object(n.e)("There was an issue deleting %s: %s",s,a))))}($)},onHide:()=>N(null),open:!0,title:Object(n.e)("Delete Database?")}),Object(ce.jsx)(j.b,{className:"database-list-view",columns:H,count:s,data:b,fetchData:f,filters:B,initialSort:[{id:"changed_on_delta_humanized",desc:!0}],loading:t,pageSize:25}),Object(ce.jsx)(O.a,{resourceName:"database",resourceLabel:Object(n.e)("database"),passwordsNeededMessage:wa,confirmOverwriteMessage:$a,addDangerToast:e,addSuccessToast:a,onModelImport:()=>{T(!1),_()},show:k,onHide:()=>{T(!1)},passwordFields:A,setPasswordFields:U}),L&&Object(ce.jsx)(r.a,null))}))}}]);