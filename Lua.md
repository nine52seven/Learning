about Lua...
==============

> [Lua](http://www.lua.org/) is a powerful, fast, lightweight, embeddable scripting language.

Nginx + Lua
-----------

- Nginx 请求处理阶段 init, rewrite, access, content等阶段



- 常用方法
        function table.contains(table, element)
            for _, value in pairs(table) do
                if value == element then
                    return true
                end
            end
            return false
        end

        function file_exists(name)
            local f=io.open(name,"r")
            if f~=nil then io.close(f) return true else return false end
        end


END,GOOD LUCK!
--------------
