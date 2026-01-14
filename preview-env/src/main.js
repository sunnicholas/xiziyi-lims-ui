import Vue from 'vue'
import App from './App.vue'
import router from './router'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'

// 模拟 RuoYi 的一些全局组件
import Pagination from "@/components/Pagination";
Vue.component('Pagination', Pagination)

import RightToolbar from "@/components/RightToolbar"
Vue.component('RightToolbar', RightToolbar)

// 模拟字典标签组件
Vue.component('DictTag', {
  props: ['options', 'value'],
  template: '<span>{{ label }}</span>',
  computed: {
    label() {
      if (!this.options) return this.value;
      const found = this.options.find(opt => opt.value == this.value);
      return found ? found.label : this.value;
    }
  }
})

// 模拟常用工具函数
Vue.prototype.parseTime = function(time, pattern) {
    if (arguments.length === 0 || !time) {
        return null
    }
    const format = pattern || '{y}-{m}-{d} {h}:{i}:{s}'
    let date
    if (typeof time === 'object') {
        date = time
    } else {
        if ((typeof time === 'string') && (/^[0-9]+$/.test(time))) {
            time = parseInt(time)
        }
        if ((typeof time === 'number') && (time.toString().length === 10)) {
            time = time * 1000
        }
        date = new Date(time)
    }
    const formatObj = {
        y: date.getFullYear(),
        m: date.getMonth() + 1,
        d: date.getDate(),
        h: date.getHours(),
        i: date.getMinutes(),
        s: date.getSeconds(),
        a: date.getDay()
    }
    const time_str = format.replace(/{(y|m|d|h|i|s|a)+}/g, (result, key) => {
        let value = formatObj[key]
        // Note: getDay() returns 0 on Sunday
        if (key === 'a') { return ['日', '一', '二', '三', '四', '五', '六'][value ] }
        if (result.length > 0 && value < 10) {
            value = '0' + value
        }
        return value || 0
    })
    return time_str
}

Vue.prototype.resetForm = function(refName) {
  if (this.$refs[refName]) {
    this.$refs[refName].resetFields();
  }
}

Vue.config.productionTip = false
Vue.use(ElementUI)

new Vue({
  router,
  render: h => h(App)
}).$mount('#app')
