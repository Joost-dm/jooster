import Vue from 'vue'
import VueRouter from 'vue-router'
import Login from '../views/auth/Login'
import Register from '../views/auth/Register'
import TrainingView from '../views/TrainingView'
import ForumCreate from '../components/forum/ForumCreate'
import Forum from '../views/forum/Forum'
import UsersList from '../components/forum/UsersList'

Vue.use(VueRouter)

const forumDefaults = {
  forumId: +localStorage.getItem('currentForumId'),
  branchId: +localStorage.getItem('currentBranchId'),
  threadId: +localStorage.getItem('currentThreadId')
}
var forumDefaultsURL
if (forumDefaults.forumId) {
  forumDefaultsURL = '/forum/' + forumDefaults.forumId + '/' + forumDefaults.branchId + '/' + forumDefaults.threadId
} else {
  forumDefaultsURL = '/forum/1/1/1'
}

const routes = [
  {
    path: '',
    redirect: forumDefaultsURL
  },
  {
    path: '/training',
    name: 'Training',
    component: TrainingView
  },
  {
    path: '/users',
    name: 'UserList',
    component: UsersList
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/register',
    name: 'Register',
    component: Register
  },
  {
    path: '/forum/forum/add',
    name: 'ForumCreate',
    component: ForumCreate
  },
  {
    path: '/forum/',
    redirect: forumDefaultsURL
  },
  {
    path: '/forum/:forumId?/:branchId?/:threadId?',
    name: 'Forum',
    props: true,
    component: Forum
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
