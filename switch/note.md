
### 2️⃣ 赋予执行权限

<pre class="overflow-visible!" data-start="1558" data-end="1600"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-bash"><span><span>chmod</span><span> +x ~/git-proxy-toggle.sh
</span></span></code></div></div></pre>

---

### 3️⃣ 使用命令

#### ✅ 开启代理

<pre class="overflow-visible!" data-start="1633" data-end="1674"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-bash"><span><span>bash ~/git-proxy-toggle.sh on
</span></span></code></div></div></pre>

#### ✅ 关闭代理

<pre class="overflow-visible!" data-start="1688" data-end="1730"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-bash"><span><span>bash ~/git-proxy-toggle.sh off
</span></span></code></div></div></pre>

#### ✅ 查看状态

<pre class="overflow-visible!" data-start="1744" data-end="1789"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-bash"><span><span>bash ~/git-proxy-toggle.sh status
</span></span></code></div></div></pre>

---

## 🧠 三、（可选）添加到全局命令

如果你希望像命令一样随时输入：

<pre class="overflow-visible!" data-start="1833" data-end="1888"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-bash"><span><span>git-proxy on
git-proxy off
git-proxy status
</span></span></code></div></div></pre>

可以把脚本移动到 `/usr/local/bin` 并改名：

<pre class="overflow-visible!" data-start="1922" data-end="2027"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-bash"><span><span>sudo </span><span>mv</span><span> ~/git-proxy-toggle.sh /usr/local/bin/git-proxy
sudo </span><span>chmod</span><span> +x /usr/local/bin/git-proxy
</span></span></code></div></div></pre>

现在你在任何目录都能直接执行：

<pre class="overflow-visible!" data-start="2045" data-end="2100"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-bash"><span><span>git-proxy on
git-proxy off
git-proxy status</span></span></code></div></div></pre>
