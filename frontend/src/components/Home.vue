<template>
  <div>
    <el-container>
      <el-header style="background-color: #FAFADA">
        <div v-if="hasLogin">
          <span>current user: {{ username }}</span>
          <span> email: {{ email }}</span>
          <el-button :loading="loading" type="text" @click.native.prevent="handleLogout">Logout</el-button>
        </div>
        <div v-else>
          <el-button type="primary" @click.native.prevent="showLoginDialog=true">sign in</el-button>
          <el-button type="primary" @click.native.prevent="showRegisterDialog=true">register</el-button>
        </div>
      </el-header>
      <el-main>
        <el-dialog title="Register" :visible.sync="showRegisterDialog">
          <el-form ref="registerForm" :model="registerForm" autocomplete="on"
                   label-position="left">
            <el-form-item prop="username">
              <el-input
                ref="username"
                v-model="registerForm.username"
                placeholder="Username"
                name="username"
                type="text"
                tabindex="1"
                autocomplete="on"
              />
            </el-form-item>
            <el-form-item prop="email">
              <el-input
                ref="email"
                v-model="registerForm.email"
                placeholder="email"
                name="email"
                type="email"
                tabindex="1"
                autocomplete="on"
              />
            </el-form-item>
            <el-form-item prop="password">
              <el-input
                :key="passwordType"
                ref="password"
                v-model="registerForm.password"
                :type="passwordType"
                placeholder="Password"
                name="password"
                tabindex="2"
                autocomplete="on"
                @blur="capsTooltip = false"
              />
            </el-form-item>
            <el-button :loading="loading" type="primary" style="width:40%;margin-bottom:30px;"
                       @click.native.prevent="handleRegister">Register
            </el-button>
            <el-button :loading="loading" type="primary" style="width:40%;margin-bottom:30px;"
                       @click.native.prevent="showLoginDialog=true;showRegisterDialog=false"> Go Login
            </el-button>
          </el-form>
        </el-dialog>


        <el-dialog title="Login" :visible.sync="showLoginDialog">
          <el-form ref="loginForm" :model="loginForm" autocomplete="on"
                   label-position="left">
            <el-form-item prop="username">
              <el-input
                ref="username"
                v-model="loginForm.username"
                placeholder="Username or email"
                name="username"
                type="text"
                tabindex="1"
                autocomplete="on"
              />
            </el-form-item>
            <el-form-item prop="password">
              <el-input
                :key="passwordType"
                ref="password"
                v-model="loginForm.password"
                :type="passwordType"
                placeholder="Password"
                name="password"
                tabindex="2"
                autocomplete="on"
                @blur="capsTooltip = false"
                @keyup.enter.native="handleLogin"
              />
            </el-form-item>
            <el-form-item prop="password">
              <el-checkbox v-model="loginForm.remember">remember me</el-checkbox>
            </el-form-item>

            <el-button :loading="loading" type="primary" style="width:40%;margin-bottom:30px;"
                       @click.native.prevent="handleLogin">Login
            </el-button>
            <el-button :loading="loading" type="primary" style="width:40%;margin-bottom:30px;"
                       @click.native.prevent="showLoginDialog=false;showRegisterDialog=true"> Go Register
            </el-button>
          </el-form>
        </el-dialog>

        <el-dialog title="Add comment" :visible.sync="showCommentDialog">
          <el-form ref="commentForm" :model="commentForm">
            <el-form-item prop="content">
              <el-input
                ref="content"
                v-model="commentForm.content"
                placeholder="you can put 3 ~ 300 chars"
                name="content"
                type="textarea"
                :maxlength="300"
                tabindex="1"
                :rows="5"
                :autosize="{ minRows: 5}"
                @input="commentChange"
              />
            </el-form-item>
            <span>Remaining words: {{remaining_words}}</span>

            <el-button :loading="loading" type="primary" style="width:40%;margin-bottom:30px;"
                       @click.native.prevent="addComments">comment
            </el-button>
          </el-form>
        </el-dialog>

        <el-button type="primary" @click.native.prevent="initCommentForm">AddComments</el-button>

        <ul style="overflow:auto">
          <li v-for="comment in comments">
            <div style="text-align: left;">
              <p>
                <span v-for="i in comment.depth">&nbsp-----</span>{{ comment.username }} say:( {{ comment.created }})
              </p>
              <p>
                <span v-for="i in comment.depth">&nbsp-----</span>{{ comment.content }}
                <el-button @click.native.prevent="addReplay(comment.id)">reply</el-button>
              </p>
            </div>

          </li>
        </ul>

      </el-main>
    </el-container>
  </div>
</template>

<script>
import {validUsername} from '../utils/validate'

import axios from 'axios'

axios.defaults.withCredentials = true
export default {
  data () {
    const validateUsername = (rule, value, callback) => {
      if (!validUsername(value)) {
        callback(new Error('Please enter the correct user name'))
      } else {
        callback()
      }
    }
    const validatePassword = (rule, value, callback) => {
      if (value.length < 8) {
        callback(new Error('The password can not be less than 6 chars.'))
      } else {
        callback()
      }
    }
    return {
      registerForm: {
        username: 'admin',
        password: '111111Ad@',
        email: 'abc@qq.com'
      },
      loginForm: {
        username: 'admin',
        password: '111111Ad@',
        remember: false
      },
      loginRules: {
        username: [{required: true, trigger: 'blur', validator: validateUsername}],
        password: [{required: true, trigger: 'blur', validator: validatePassword}]
      },
      username: '',
      email: '',
      passwordType: 'password',
      capsTooltip: false,
      loading: false,
      showRegisterDialog: false,
      hasLogin: false,
      showLoginDialog: false,
      showCommentDialog: false,
      commentForm: {
        content: '',
        parent: 0
      },
      comments: [],
      remaining_words: 300

    }
  },
  methods: {

    handleRegister () {
      const path = `http://127.0.0.1:5000/api/auth/register`
      const reqData = {
        username: this.registerForm.username.trim(),
        password: this.registerForm.password.trim(),
        email: this.registerForm.email.trim()
      }
      axios.post(path, reqData)
        .then(response => {
          if (response.data.code === 201) {
            this.$message.success(response.data.msg)
            this.showRegisterDialog = false
            this.showLoginDialog = true
            this.loginForm.username = this.registerForm.username
            this.loginForm.password = this.registerForm.password
          } else {
            this.$message.error(response.data.msg)
          }
        })
        .catch(error => {
          console.log(error)
        })
    },
    handleLogin () {
      const path = `http://127.0.0.1:5000/api/auth/login`
      const reqData = {
        username: this.loginForm.username.trim(),
        password: this.loginForm.password.trim(),
        remember: this.loginForm.remember
      }
      axios.post(path, reqData)
        .then(response => {
          if (response.data.code === 200) {
            this.$message.success('login success')
            this.showLoginDialog = false
            this.getUserInfo()
          } else {
            this.$message.error(response.data.msg)
          }
        })
        .catch(error => {
          console.log(error)
        })
    },
    handleLogout () {
      const path = `http://127.0.0.1:5000/api/auth/logout`
      axios.post(path, {username: this.loginForm.username.trim(), password: this.loginForm.password})
        .then(response => {
          if (response.data.code === 200) {
            this.hasLogin = false
            this.username = ''
            this.email = ''
          }
        })
        .catch(error => {
          console.log(error)
        })
    },
    getUserInfo () {
      const path = `http://127.0.0.1:5000/api/auth/info`
      axios.get(path)
        .then(response => {
          const resData = response.data
          console.log(resData)
          if (resData.code === 200) {
            this.username = resData.data.username
            this.email = resData.data.email
            this.hasLogin = true
          } else {
            console.log('未登入')
            this.showLoginDialog = true
          }
        })
        .catch(error => {
          console.log('get user info error', error)
        })
    },
    getComments () {
      const path = `http://127.0.0.1:5000/api/comment`
      axios.get(path)
        .then(response => {
          if (response.data.code === 200) {
            this.comments = response.data.data
          } else {
            this.$message.error(response.data.msg)
          }
        })
        .catch(error => {
          console.log(error)
        })
    },
    initCommentForm () {
      this.commentForm.parent = 0
      this.commentForm.content = ''
      this.showCommentDialog = true
    },
    addComments () {
      const path = `http://127.0.0.1:5000/api/comment/`
      const reqData = {
        content: this.commentForm.content,
        parent: this.commentForm.parent
      }
      axios.post(path, reqData)
        .then(response => {
          if (response.data.code === 201) {
            this.$message.success(response.data.msg)
            this.showCommentDialog = false
            this.getComments()
          } else {
            this.$message.error(response.data.msg)
          }
        })
        .catch(error => {
          console.log(error)
        })
    },
    addReplay (parentId) {
      console.log({parentId})
      this.commentForm.parent = parentId
      this.commentForm.content = ''
      this.commentForm.parent = parentId
      this.showCommentDialog = true
    },
    commentChange () {
      this.remaining_words = 300 - this.commentForm.content.length
    }
  },
  mounted () {
    this.getUserInfo()
    this.getComments()
  }
}
</script>
